[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot

# Select the newest supported 64-bit CPython, while keeping Python 3.10 as the
# minimum supported server runtime.
$PythonSelector = $null
foreach ($Version in @('3.14', '3.13', '3.12', '3.11', '3.10')) {
    & py "-$Version" -c 'import sys; raise SystemExit(0 if sys.maxsize > 2**32 else 1)' 2>$null
    if ($LASTEXITCODE -eq 0) {
        $PythonSelector = "-$Version"
        break
    }
}
if ($null -eq $PythonSelector) {
    throw 'Python 3.10-3.14 x64 and the Windows py launcher are required.'
}

$VirtualEnvironment = Join-Path $Root '.venv'
# The virtual environment is generated state. Recreating it prevents an old
# deployment from retaining stale packages or an unsupported Python runtime.
if (Test-Path -LiteralPath $VirtualEnvironment) {
    Remove-Item -LiteralPath $VirtualEnvironment -Recurse -Force
}
& py $PythonSelector -m venv $VirtualEnvironment
if ($LASTEXITCODE -ne 0) { throw 'Could not create the Python virtual environment.' }

$Python = Join-Path $VirtualEnvironment 'Scripts\python.exe'
$SdkWheel = Join-Path $Root 'wheels\__SDK_WHEEL__'
$RuntimeWheel = Join-Path $Root 'wheels\__RUNTIME_WHEEL__'
foreach ($Wheel in @($SdkWheel, $RuntimeWheel)) {
    if (-not (Test-Path -LiteralPath $Wheel -PathType Leaf)) {
        throw "Release wheel is missing: $Wheel"
    }
}

# Pin the two project wheels by exact filename and resolve every dependency
# from the bundled wheel directory, so installation never needs the network.
& $Python -m pip install `
    --disable-pip-version-check `
    --no-index `
    --find-links (Join-Path $Root 'wheels') `
    --force-reinstall `
    $RuntimeWheel `
    $SdkWheel
if ($LASTEXITCODE -ne 0) { throw 'Offline Python package installation failed.' }

$ServiceRoot = Join-Path $Root 'integrations\customer-service-api'
$ModelTemplate = Join-Path $ServiceRoot 'customer-service.model.example.json'
$ModelConfig = Join-Path $ServiceRoot 'customer-service.model.json'
if (-not (Test-Path -LiteralPath $ModelConfig)) {
    Copy-Item -LiteralPath $ModelTemplate -Destination $ModelConfig
}
foreach ($Directory in @('data\dsh-home', 'skills', 'workspace')) {
    New-Item -ItemType Directory -Path (Join-Path $Root $Directory) -Force | Out-Null
}

Write-Host ''
Write-Host 'Installation completed.' -ForegroundColor Green
Write-Host "Edit model configuration: $ModelConfig"
Write-Host 'Then start the service with: powershell -ExecutionPolicy Bypass -File .\start.ps1'
