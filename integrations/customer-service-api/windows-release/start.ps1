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

function Get-JsonProperty {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $Property = $Object.PSObject.Properties[$Name]
    if ($null -eq $Property) {
        return $null
    }
    return $Property.Value
}

function Write-ConfigurationValue {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        $Value
    )

    $Text = if ($null -eq $Value -or [string]::IsNullOrWhiteSpace([string]$Value)) {
        '<empty>'
    }
    else {
        [string]$Value
    }
    Write-Host ("  {0}: {1}" -f $Name, $Text)
}

function Write-ModelConfiguration {
    param([Parameter(Mandatory = $true)][string]$Path)

    $Model = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    Write-Host 'Model configuration:'
    foreach ($Name in @(
        'provider',
        'model',
        'displayName',
        'baseUrl',
        'businessDataMode',
        'apiMcpUrl',
        'apiMcpToolCallTimeoutMilliseconds',
        'apiMcpFailOnStartupError',
        'databaseMaxCatalogTables',
        'contextWindow',
        'maxOutputTokens',
        'reasoningEffort',
        'requestMaxTokens',
        'timeoutMilliseconds'
    )) {
        Write-ConfigurationValue $Name (Get-JsonProperty $Model $Name)
    }
    $ApiKey = Get-JsonProperty $Model 'apiKey'
    $ApiKeyStatus = if ($null -eq $ApiKey -or [string]::IsNullOrWhiteSpace([string]$ApiKey)) {
        '<empty>'
    }
    else {
        '<configured>'
    }
    Write-ConfigurationValue 'apiKey' $ApiKeyStatus
}

function Write-StartupConfiguration {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Python,
        [Parameter(Mandatory = $true)][string]$Runtime,
        [Parameter(Mandatory = $true)][string]$RuntimeRg,
        [Parameter(Mandatory = $true)][string]$Server,
        [Parameter(Mandatory = $true)][string]$ModelConfig,
        [Parameter(Mandatory = $true)][string]$EffectiveDshBin
    )

    Write-Host 'Runtime configuration:'
    Write-ConfigurationValue 'Root' $Root
    Write-ConfigurationValue 'Python' $Python
    Write-ConfigurationValue 'Runtime' $Runtime
    Write-ConfigurationValue 'Runtime rg' $RuntimeRg
    Write-ConfigurationValue 'Effective DSH bin' $EffectiveDshBin
    Write-ConfigurationValue 'Server' $Server
    Write-ConfigurationValue 'Model config' $ModelConfig
    foreach ($Name in @(
        'DCS_DSH_HOME',
        'DCS_SKILL_DIR',
        'DCS_WORKSPACE',
        'DCS_MCP_URL',
        'DCS_HOST',
        'DCS_PORT',
        'DCS_DSH_BIN',
        'DCS_MODEL_CONFIG_FILE'
    )) {
        Write-ConfigurationValue $Name ([Environment]::GetEnvironmentVariable($Name))
    }
    Write-ModelConfiguration $ModelConfig
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
Set-DefaultEnvironmentVariable 'DCS_MCP_URL' 'http://127.0.0.1:5301/mcp'
Set-DefaultEnvironmentVariable 'DCS_HOST' '127.0.0.1'
Set-DefaultEnvironmentVariable 'DCS_PORT' '8765'
Set-DefaultEnvironmentVariable 'DCS_DSH_BIN' $Runtime
Set-DefaultEnvironmentVariable 'DCS_MODEL_CONFIG_FILE' $ModelConfig

$EffectiveDshBin = [Environment]::GetEnvironmentVariable('DCS_DSH_BIN')
$EffectiveModelConfig = [Environment]::GetEnvironmentVariable('DCS_MODEL_CONFIG_FILE')
if (-not (Test-Path -LiteralPath $EffectiveDshBin -PathType Leaf)) {
    throw "DCS_DSH_BIN does not exist: $EffectiveDshBin"
}
if (-not (Test-Path -LiteralPath $EffectiveModelConfig -PathType Leaf)) {
    throw "DCS_MODEL_CONFIG_FILE does not exist: $EffectiveModelConfig"
}

Write-StartupConfiguration $Root $Python $Runtime $RuntimeRg $Server $EffectiveModelConfig $EffectiveDshBin
Write-Host "Starting customer-service API: http://$($env:DCS_HOST):$($env:DCS_PORT)" -ForegroundColor Green
Write-Host "Health endpoint: http://$($env:DCS_HOST):$($env:DCS_PORT)/health/live"
& $Python $Server
if ($LASTEXITCODE -ne 0) {
    throw "The customer-service API exited with code $LASTEXITCODE."
}
