[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Set-DefaultEnvironmentVariable {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Value
    )

    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable($Name))) {
        [Environment]::SetEnvironmentVariable($Name, $Value)
    }
}

# Use the bundled native runtime directly so no wrapper can close the SDK pipe.
$Root = $PSScriptRoot
$Python = Join-Path $Root '.venv\Scripts\python.exe'
$Runtime = Join-Path $Root 'runtime\deepseek-harness-sdk-runtime-win-x64.exe'
$RuntimeRg = Join-Path $Root 'runtime\deepseek-harness-sdk-runtime-win-x64-rg.exe'
$ServiceDirectory = Join-Path $Root 'integrations\customer-service-api'
$Server = Join-Path $ServiceDirectory 'server.py'
$ModelConfig = Join-Path $ServiceDirectory 'customer-service.model.json'

foreach ($RequiredFile in @($Python, $Runtime, $RuntimeRg)) {
    if (-not (Test-Path -LiteralPath $RequiredFile -PathType Leaf)) {
        throw 'The runtime is not installed. Run .\install.ps1 first.'
    }
}
if (-not (Test-Path -LiteralPath $ModelConfig -PathType Leaf)) {
    throw 'customer-service.model.json is missing. Run .\install.ps1 and complete the model configuration.'
}

# Preserve operator-supplied environment settings and provide package defaults.
Set-DefaultEnvironmentVariable 'DCS_DSH_HOME' (Join-Path $Root 'data\dsh-home')
Set-DefaultEnvironmentVariable 'DCS_SKILL_DIR' (Join-Path $Root 'skills')
Set-DefaultEnvironmentVariable 'DCS_WORKSPACE' (Join-Path $Root 'workspace')
Set-DefaultEnvironmentVariable 'DCS_HOST' '127.0.0.1'
Set-DefaultEnvironmentVariable 'DCS_PORT' '8765'
Set-DefaultEnvironmentVariable 'DCS_DSH_BIN' $Runtime
Set-DefaultEnvironmentVariable 'DCS_MODEL_CONFIG_FILE' $ModelConfig

Write-Host "Starting customer-service API: http://$($env:DCS_HOST):$($env:DCS_PORT)" -ForegroundColor Green
Write-Host "Health endpoint: http://$($env:DCS_HOST):$($env:DCS_PORT)/health/live"
& $Python $Server
if ($LASTEXITCODE -ne 0) {
    throw "The customer-service API exited with code $LASTEXITCODE."
}
