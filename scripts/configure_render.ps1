<#
.SYNOPSIS
  Ensure the Render web service has API_KEY set (and optionally redeploy).

.DESCRIPTION
  Requires a Render *account* API key (Dashboard → Account Settings → API Keys),
  NOT the worker's own API_KEY.

  Usage:
    $env:RENDER_API_KEY = "rnd_..."
    .\scripts\configure_render.ps1

  Optional:
    $env:WORKER_API_KEY = "your-chosen-worker-bearer-token"   # else one is generated
    $env:RENDER_SERVICE_NAME = "vibe23-energyplus-worker"
#>
param(
    [string]$ServiceName = $(if ($env:RENDER_SERVICE_NAME) { $env:RENDER_SERVICE_NAME } else { "vibe23-energyplus-worker" }),
    [switch]$SkipRedeploy
)

$ErrorActionPreference = "Stop"
$accountKey = $env:RENDER_API_KEY
if (-not $accountKey) {
    throw "Set RENDER_API_KEY to your Render account API key (Account Settings → API Keys)."
}

$headers = @{
    Authorization = "Bearer $accountKey"
    Accept        = "application/json"
    "Content-Type" = "application/json"
}

Write-Host "Listing services…"
$services = Invoke-RestMethod -Uri "https://api.render.com/v1/services?limit=50" -Headers $headers
$match = $services | Where-Object {
    $svc = if ($_.service) { $_.service } else { $_ }
    $svc.name -eq $ServiceName
} | Select-Object -First 1

if (-not $match) {
    Write-Host "Services returned:" ($services | ConvertTo-Json -Depth 4)
    throw "Service named '$ServiceName' not found."
}

$svc = if ($match.service) { $match.service } else { $match }
$serviceId = $svc.id
Write-Host "Found $ServiceName → $serviceId"

$workerKey = $env:WORKER_API_KEY
if (-not $workerKey) {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $workerKey = ([Convert]::ToBase64String($bytes) -replace '[+/=]', 'x')
    Write-Host "Generated WORKER_API_KEY (save this for Streamlit secrets)."
}

$body = @(
    @{ key = "API_KEY"; value = $workerKey }
    @{ key = "MAX_CONCURRENT_JOBS"; value = "1" }
    @{ key = "JOB_TTL_HOURS"; value = "24" }
    @{ key = "MAX_UPLOAD_MB"; value = "50" }
    @{ key = "SIM_TIMEOUT_SECONDS"; value = "900" }
) | ConvertTo-Json -Depth 5

Write-Host "PUT env-vars…"
Invoke-RestMethod -Method Put `
    -Uri "https://api.render.com/v1/services/$serviceId/env-vars" `
    -Headers $headers `
    -Body $body | Out-Null

Write-Host "API_KEY configured on service."

if (-not $SkipRedeploy) {
    Write-Host "Triggering deploy…"
    Invoke-RestMethod -Method Post `
        -Uri "https://api.render.com/v1/services/$serviceId/deploys" `
        -Headers $headers `
        -Body "{}" | Out-Null
}

$out = Join-Path $PSScriptRoot "..\.env.render.local"
@"
# Generated $(Get-Date -Format o) — gitignored. Use in Streamlit secrets / local tests.
EPLUS_WORKER_URL=https://vibe23-energyplus-worker.onrender.com
EPLUS_WORKER_API_KEY=$workerKey
RENDER_SERVICE_ID=$serviceId
"@ | Set-Content -Path $out -Encoding utf8

Write-Host "Wrote $out"
Write-Host "Streamlit Community Cloud secrets.toml:"
Write-Host 'EPLUS_WORKER_URL = "https://vibe23-energyplus-worker.onrender.com"'
Write-Host "EPLUS_WORKER_API_KEY = `"$workerKey`""
Write-Host "Done. After deploy finishes, curl /healthz and expect api_key_configured=true."
