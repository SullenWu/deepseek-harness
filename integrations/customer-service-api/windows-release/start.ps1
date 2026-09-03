[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot

function Set-DefaultEnvironmentVariable {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Value
    )

    # Preserve an operator-provided value; only fill release-local defaults.
    $Existing = [Environment]::GetEnvironmentVariable($Name, 'Process')
    if ([string]::IsNullOrWhiteSpace($Existing)) {
        [Environment]::SetEnvironmentVariable($Name, $Value, 'Process')
    }
}

$Python = Join-Path $Root '.venv\Scripts\python.exe'
$Runtime = Join-Path $Root 'runtime\deepseek-harness-sdk-runtime-win-x64.exe'
$RuntimeSearch = Join-Path $Root 'runtime\deepseek-harness-sdk-runtime-win-x64-rg.exe'
$Server = Join-Path $Root 'integrations\customer-service-api\server.py'
# Start the native runtime directly. The Python dsh.exe console wrapper can
# close the SDK stdio transport early on Windows, and the runtime requires its
# adjacent ripgrep sidecar for product-skill searches.
foreach ($RequiredFile in @($Python, $Runtime, $RuntimeSearch, $Server)) {
    if (-not (Test-Path -LiteralPath $RequiredFile -PathType Leaf)) {
        throw "Required file is missing: $RequiredFile. Run install.ps1 first."
    }
}

Set-DefaultEnvironmentVariable 'DCS_DSH_HOME' (Join-Path $Root 'data\dsh-home')
Set-DefaultEnvironmentVariable 'DCS_SKILL_DIR' (Join-Path $Root 'skills')
Set-DefaultEnvironmentVariable 'DCS_WORKSPACE' (Join-Path $Root 'workspace')
Set-DefaultEnvironmentVariable 'DCS_MODEL_CONFIG_FILE' (Join-Path $Root 'integrations\customer-service-api\customer-service.model.json')
Set-DefaultEnvironmentVariable 'DCS_DSH_BIN' $Runtime
Set-DefaultEnvironmentVariable 'DCS_HOST' '127.0.0.1'
Set-DefaultEnvironmentVariable 'DCS_PORT' '8765'

& $Python $Server
if ($LASTEXITCODE -ne 0) { throw "Customer-service API exited with code $LASTEXITCODE." }
