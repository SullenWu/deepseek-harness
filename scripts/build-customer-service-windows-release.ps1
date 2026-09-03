[CmdletBinding()]
param(
    [ValidatePattern('^[A-Za-z0-9._-]+$')]
    [string]$OutputDirectory = 'dist-customer-service-windows',
    [switch]$SkipInstall,
    [switch]$SkipRuntimeBuild,
    [switch]$KeepStaging
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# This release is deliberately built on Windows: the native node-pty addon and
# the pkg-produced executable must both match the target operating system.
$Root = Split-Path -Parent $PSScriptRoot
$OutputRoot = Join-Path $Root $OutputDirectory
$StagingRoot = Join-Path $OutputRoot '.staging'
$WheelRoot = Join-Path $OutputRoot '.wheels'
$RuntimeName = 'deepseek-harness-sdk-runtime-win-x64.exe'
$RuntimeRgName = 'deepseek-harness-sdk-runtime-win-x64-rg.exe'

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    Write-Host "==> $Label"
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE."
    }
}

function Remove-GeneratedPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    # Refuse to remove anything outside the dedicated output directory.
    $ResolvedOutput = [System.IO.Path]::GetFullPath($OutputRoot).TrimEnd('\') + '\'
    $ResolvedTarget = [System.IO.Path]::GetFullPath($Path)
    if (-not $ResolvedTarget.StartsWith($ResolvedOutput, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove a path outside the generated output directory: $ResolvedTarget"
    }
    if (Test-Path -LiteralPath $ResolvedTarget) {
        Remove-Item -LiteralPath $ResolvedTarget -Recurse -Force
    }
}

if ($env:OS -ne 'Windows_NT') {
    throw 'This release must be built on a Windows x64 computer.'
}
if (-not [Environment]::Is64BitProcess) {
    throw 'Use a 64-bit PowerShell process.'
}

Push-Location $Root
try {
    $NodeVersion = (& node --version).Trim()
    if ($LASTEXITCODE -ne 0 -or $NodeVersion -notmatch '^v24\.') {
        throw "Node.js 24 x64 is required; found '$NodeVersion'."
    }
    $NodeArchitecture = (& node -p 'process.arch').Trim()
    if ($LASTEXITCODE -ne 0 -or $NodeArchitecture -ne 'x64') {
        throw "Node.js 24 x64 is required; found architecture '$NodeArchitecture'."
    }
    $PnpmVersion = (& pnpm --version).Trim()
    if ($LASTEXITCODE -ne 0 -or $PnpmVersion -ne '11.7.0') {
        throw "pnpm 11.7.0 is required; found '$PnpmVersion'. Run: corepack prepare pnpm@11.7.0 --activate"
    }

    # pkg needs Windows symlink support while it stages the dependency closure.
    $DeveloperMode = Get-ItemPropertyValue `
        -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' `
        -Name 'AllowDevelopmentWithoutDevLicense' `
        -ErrorAction SilentlyContinue
    if ($DeveloperMode -ne 1) {
        throw 'Windows Developer Mode is required. Enable it in Settings > System > For developers.'
    }

    $PythonExe = (& py -3.10 -c 'import sys; assert sys.maxsize > 2**32; print(sys.executable)').Trim()
    if ($LASTEXITCODE -ne 0 -or -not $PythonExe) {
        throw 'Python 3.10 x64 and the py launcher are required.'
    }
    $PythonScripts = (& py -3.10 -c 'import sysconfig; print(sysconfig.get_path("scripts"))').Trim()
    if ($LASTEXITCODE -ne 0 -or -not $PythonScripts) {
        throw 'Could not locate the Python 3.10 Scripts directory.'
    }

    Invoke-CheckedCommand 'Install uv 0.11.23' 'py' @('-3.10', '-m', 'pip', 'install', '--disable-pip-version-check', 'uv==0.11.23')
    $env:PATH = "$PythonScripts;$env:PATH"
    Invoke-CheckedCommand 'Verify uv' 'uv' @('--version')

    if (-not $SkipInstall) {
        Invoke-CheckedCommand 'Install repository dependencies' 'pnpm' @('install', '--frozen-lockfile')
    }

    if (-not $SkipRuntimeBuild) {
        $env:DSH_BUILD_CLIENT_PROFILE = 'official'
        Invoke-CheckedCommand `
            'Build Windows runtime executables' `
            'pnpm' `
            @('exec', 'tsx', 'scripts/build-exe-for-python-sdk.ts', '--targets=node24-win-x64')
    }

    $RuntimeSource = Join-Path $Root "dist-exe\$RuntimeName"
    $RuntimeRgSource = Join-Path $Root "dist-exe\$RuntimeRgName"
    foreach ($RequiredRuntime in @($RuntimeSource, $RuntimeRgSource)) {
        if (-not (Test-Path -LiteralPath $RequiredRuntime -PathType Leaf)) {
            throw "Required runtime executable is missing: $RequiredRuntime"
        }
    }

    $Package = Get-Content -LiteralPath (Join-Path $Root 'package.json') -Raw | ConvertFrom-Json
    $Version = [string]$Package.version
    if ($Version -notmatch '^\d+\.\d+\.\d+(?:-(?:a|b|c|rc|alpha|beta|pre|preview)\.?\d+)?$') {
        throw "Repository version '$Version' cannot be converted to a Python wheel version."
    }
    $WheelVersion = $Version
    if ($WheelVersion -match '^(?<stable>\d+\.\d+\.\d+)-(?<label>a|b|c|rc|alpha|beta|pre|preview)\.?(?<number>\d+)$') {
        $Label = switch ($Matches.label) {
            'alpha' { 'a' }
            'beta' { 'b' }
            'c' { 'rc' }
            'pre' { 'rc' }
            'preview' { 'rc' }
            default { $Matches.label }
        }
        $WheelVersion = "$($Matches.stable)$Label$($Matches.number)"
    }

    New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
    Remove-GeneratedPath $StagingRoot
    Remove-GeneratedPath $WheelRoot
    New-Item -ItemType Directory -Path $StagingRoot, $WheelRoot -Force | Out-Null

    Invoke-CheckedCommand `
        'Build Python SDK wheel' `
        $PythonExe `
        @('scripts/build-python-release.py', '--package', 'sdk', '--output-dir', $WheelRoot)
    Invoke-CheckedCommand `
        'Build Windows runtime wheel' `
        $PythonExe `
        @(
            'scripts/build-python-release.py',
            '--package', 'runtime',
            '--platform', 'win-x64',
            '--runtime-exe', $RuntimeSource,
            '--output-dir', $WheelRoot
        )

    # Download one binary dependency closure for every supported server Python ABI.
    foreach ($Abi in @('310', '311', '312', '313', '314')) {
        Invoke-CheckedCommand `
            "Download Python $($Abi.Substring(0, 1)).$($Abi.Substring(1)) dependencies" `
            $PythonExe `
            @(
                '-m', 'pip', 'download',
                '--disable-pip-version-check',
                '--dest', $WheelRoot,
                '--only-binary=:all:',
                '--platform', 'win_amd64',
                '--implementation', 'cp',
                '--python-version', $Abi,
                '--abi', "cp$Abi",
                'pydantic>=2.12,<3'
            )
    }

    $ReleaseName = "deepseek-harness-customer-service-$Version-win-x64-exe-visible"
    $ReleaseRoot = Join-Path $StagingRoot $ReleaseName
    $RuntimeRoot = Join-Path $ReleaseRoot 'runtime'
    $ReleaseWheelRoot = Join-Path $ReleaseRoot 'wheels'
    $ServiceRoot = Join-Path $ReleaseRoot 'integrations\customer-service-api'
    New-Item -ItemType Directory -Path $RuntimeRoot, $ReleaseWheelRoot, $ServiceRoot -Force | Out-Null
    foreach ($Directory in @('skills', 'workspace', 'data\dsh-home')) {
        $DirectoryPath = Join-Path $ReleaseRoot $Directory
        New-Item -ItemType Directory -Path $DirectoryPath -Force | Out-Null
        Set-Content -LiteralPath (Join-Path $DirectoryPath '.gitkeep') -Value '' -Encoding Ascii
    }

    Copy-Item -LiteralPath $RuntimeSource -Destination (Join-Path $RuntimeRoot $RuntimeName)
    Copy-Item -LiteralPath $RuntimeRgSource -Destination (Join-Path $RuntimeRoot $RuntimeRgName)
    Copy-Item -Path (Join-Path $WheelRoot '*.whl') -Destination $ReleaseWheelRoot
    foreach ($Filename in @('server.py', 'cleanup_sessions.py', 'customer-service.cordis.patch.yml', 'customer-service.model.example.json', 'README.md')) {
        Copy-Item `
            -LiteralPath (Join-Path $Root "integrations\customer-service-api\$Filename") `
            -Destination (Join-Path $ServiceRoot $Filename)
    }
    Copy-Item -LiteralPath (Join-Path $Root 'LICENSE') -Destination (Join-Path $ReleaseRoot 'LICENSE')
    Copy-Item -LiteralPath (Join-Path $Root 'THIRD_PARTY_NOTICES.md') -Destination (Join-Path $ReleaseRoot 'THIRD_PARTY_NOTICES.md')

    $SdkWheelName = "deepseek_harness_sdk-$WheelVersion-py3-none-any.whl"
    $RuntimeWheelName = "deepseek_harness_runtime_bin-$WheelVersion-py3-none-win_amd64.whl"
    foreach ($WheelName in @($SdkWheelName, $RuntimeWheelName)) {
        if (-not (Test-Path -LiteralPath (Join-Path $ReleaseWheelRoot $WheelName) -PathType Leaf)) {
            throw "Expected wheel is missing: $WheelName"
        }
    }

    $TemplateRoot = Join-Path $Root 'integrations\customer-service-api\windows-release'
    $InstallTemplate = Get-Content -LiteralPath (Join-Path $TemplateRoot 'install.ps1') -Raw
    $InstallScript = $InstallTemplate.Replace('__SDK_WHEEL__', $SdkWheelName).Replace('__RUNTIME_WHEEL__', $RuntimeWheelName)
    Set-Content -LiteralPath (Join-Path $ReleaseRoot 'install.ps1') -Value $InstallScript -Encoding Ascii
    Copy-Item -LiteralPath (Join-Path $TemplateRoot 'start.ps1') -Destination (Join-Path $ReleaseRoot 'start.ps1')
    Copy-Item -LiteralPath (Join-Path $TemplateRoot 'README-WINDOWS.zh.md') -Destination (Join-Path $ReleaseRoot 'README-WINDOWS.md')

    $Commit = (& git rev-parse HEAD).Trim()
    $BuildTime = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    @(
        "Release: $ReleaseName"
        "Repository version: $Version"
        "Git commit: $Commit"
        "Built at UTC: $BuildTime"
        "Node: $NodeVersion"
        "Node architecture: $NodeArchitecture"
        "pnpm: $PnpmVersion"
        'Target: node24-win-x64'
        'Python server support: CPython 3.10-3.14 x64'
    ) | Set-Content -LiteralPath (Join-Path $ReleaseRoot 'BUILD-INFO.txt') -Encoding Ascii

    $HashLines = Get-ChildItem -LiteralPath $ReleaseRoot -File -Recurse |
        Where-Object { $_.Name -ne 'SHA256SUMS.txt' } |
        Sort-Object FullName |
        ForEach-Object {
            $RelativePath = $_.FullName.Substring($ReleaseRoot.Length + 1).Replace('\', '/')
            $Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            "$Hash  $RelativePath"
        }
    $HashLines | Set-Content -LiteralPath (Join-Path $ReleaseRoot 'SHA256SUMS.txt') -Encoding Ascii

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $ZipPath = Join-Path $OutputRoot "$ReleaseName.zip"
    Remove-GeneratedPath $ZipPath
    [System.IO.Compression.ZipFile]::CreateFromDirectory(
        $StagingRoot,
        $ZipPath,
        [System.IO.Compression.CompressionLevel]::Optimal,
        $false
    )
    $ZipHash = (Get-FileHash -LiteralPath $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()

    Write-Host ''
    Write-Host 'Release completed.' -ForegroundColor Green
    Write-Host "ZIP: $ZipPath"
    Write-Host "SHA256: $ZipHash"
    if ($KeepStaging) {
        Write-Host "Unpacked staging: $ReleaseRoot"
    }
}
finally {
    Pop-Location
    if (-not $KeepStaging -and (Test-Path -LiteralPath $StagingRoot)) {
        Remove-GeneratedPath $StagingRoot
    }
    if (Test-Path -LiteralPath $WheelRoot) {
        Remove-GeneratedPath $WheelRoot
    }
}
