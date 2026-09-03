$ErrorActionPreference = "Stop"

# 直接使用发布包自带的 Windows runtime，避免 dsh.exe 包装层提前关闭 SDK 管道。
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Root ".venv\Scripts\python.exe"
$Dsh = Join-Path $Root "runtime\deepseek-harness-sdk-runtime-win-x64.exe"
$DshRg = Join-Path $Root "runtime\deepseek-harness-sdk-runtime-win-x64-rg.exe"
$ServiceDir = Join-Path $Root "integrations\customer-service-api"
$Server = Join-Path $ServiceDir "server.py"
$ModelConfig = Join-Path $ServiceDir "customer-service.model.json"

if (-not (Test-Path $Python) -or -not (Test-Path $Dsh) -or -not (Test-Path $DshRg)) {
    throw "运行时尚未安装，请先执行 .\install.ps1。"
}
if (-not (Test-Path $ModelConfig)) {
    throw "缺少 customer-service.model.json，请先执行 .\install.ps1 并填写模型配置。"
}

# 只在外部没有指定时使用发布包默认值，便于运维通过系统环境变量覆盖。
$env:DCS_DSH_HOME = if ([string]::IsNullOrWhiteSpace($env:DCS_DSH_HOME)) { Join-Path $Root "data\dsh-home" } else { $env:DCS_DSH_HOME }
$env:DCS_SKILL_DIR = if ([string]::IsNullOrWhiteSpace($env:DCS_SKILL_DIR)) { Join-Path $Root "skills" } else { $env:DCS_SKILL_DIR }
$env:DCS_WORKSPACE = if ([string]::IsNullOrWhiteSpace($env:DCS_WORKSPACE)) { Join-Path $Root "workspace" } else { $env:DCS_WORKSPACE }
$env:DCS_MCP_URL = if ([string]::IsNullOrWhiteSpace($env:DCS_MCP_URL)) { "http://127.0.0.1:5301/mcp" } else { $env:DCS_MCP_URL }
$env:DCS_HOST = if ([string]::IsNullOrWhiteSpace($env:DCS_HOST)) { "127.0.0.1" } else { $env:DCS_HOST }
$env:DCS_PORT = if ([string]::IsNullOrWhiteSpace($env:DCS_PORT)) { "8765" } else { $env:DCS_PORT }
$env:DCS_DSH_BIN = $Dsh
$env:DCS_MODEL_CONFIG_FILE = $ModelConfig

Write-Host "启动客服 API: http://$($env:DCS_HOST):$($env:DCS_PORT)" -ForegroundColor Green
Write-Host "健康检查: http://$($env:DCS_HOST):$($env:DCS_PORT)/health/live"
& $Python $Server
if ($LASTEXITCODE -ne 0) {
    throw "客服 API 进程异常退出，退出码: $LASTEXITCODE"
}
