$ErrorActionPreference = "Stop"

# Use the bundled Windows runtime directly so the dsh.exe wrapper cannot close
# the SDK pipe before the server finishes startup.
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Dsh = Join-Path $Root "runtime\deepseek-harness-sdk-runtime-win-x64.exe"
$DshRg = Join-Path $Root "runtime\deepseek-harness-sdk-runtime-win-x64-rg.exe"
$ServiceDir = Join-Path $Root "integrations\customer-service-api"
$Server = Join-Path $ServiceDir "server.py"
$ModelConfig = Join-Path $ServiceDir "customer-service.model.json"

if (-not (Test-Path $Python) -or -not (Test-Path $Dsh) -or -not (Test-Path $DshRg)) {
    throw "Runtime is not installed. Run .\install.ps1 first."
}
if (-not (Test-Path $ModelConfig)) {
    throw "Missing customer-service.model.json. Run .\install.ps1 and fill in the model configuration."
}

# Use release defaults only when the environment does not already provide them.
$env:DCS_DSH_HOME = if ([string]::IsNullOrWhiteSpace($env:DCS_DSH_HOME)) { Join-Path $Root "data\dsh-home" } else { $env:DCS_DSH_HOME }
$env:DCS_SKILL_DIR = if ([string]::IsNullOrWhiteSpace($env:DCS_SKILL_DIR)) { Join-Path $Root "skills" } else { $env:DCS_SKILL_DIR }
$env:DCS_WORKSPACE = if ([string]::IsNullOrWhiteSpace($env:DCS_WORKSPACE)) { Join-Path $Root "workspace" } else { $env:DCS_WORKSPACE }
$env:DCS_MCP_URL = if ([string]::IsNullOrWhiteSpace($env:DCS_MCP_URL)) { "http://127.0.0.1:5301/mcp" } else { $env:DCS_MCP_URL }
$env:DCS_HOST = if ([string]::IsNullOrWhiteSpace($env:DCS_HOST)) { "127.0.0.1" } else { $env:DCS_HOST }
$env:DCS_PORT = if ([string]::IsNullOrWhiteSpace($env:DCS_PORT)) { "8765" } else { $env:DCS_PORT }
$env:DCS_DSH_BIN = $Dsh
$env:DCS_MODEL_CONFIG_FILE = $ModelConfig

Write-Host "Starting customer service API: http://$($env:DCS_HOST):$($env:DCS_PORT)" -ForegroundColor Green
Write-Host "Health check: http://$($env:DCS_HOST):$($env:DCS_PORT)/health/live"
& $Python $Server
if ($LASTEXITCODE -ne 0) {
    throw "Customer service API exited with code $LASTEXITCODE."
}
