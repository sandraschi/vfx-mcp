param([switch]$Headless, [switch]$NoBrowser)
$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $PSCommandPath
$BackendPort = 11122

# Port zombie clearing
Get-NetTCPConnection -LocalPort $BackendPort -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

# Start backend via Start-Job
$BackendJob = Start-Job -Name "vfx-backend" -ScriptBlock {
    param($Root, $Port)
    Set-Location $Root
    uv run python -m vfx_mcp --serve
} -ArgumentList $ScriptRoot, $BackendPort

# Readiness poll
for ($i = 0; $i -lt 60; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/api/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($r.StatusCode -eq 200) { Write-Host "Backend ready on :$BackendPort" -ForegroundColor Green; break }
    } catch {}
    Start-Sleep 1
}

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:$BackendPort/api/health"
}

Write-Host "vfx-mcp running. Press Ctrl+C to stop." -ForegroundColor Cyan

# Keep-alive
while ($true) {
    if ($BackendJob.State -eq "Completed" -or $BackendJob.State -eq "Failed") {
        Receive-Job $BackendJob; break
    }
    Start-Sleep 2
}
