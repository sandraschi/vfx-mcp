# Troubleshooting

## FFmpeg not found

Ensure FFmpeg is installed and on PATH:
```powershell
ffmpeg -version
```

Set a custom path:
```
VFX_MCP_FFMPEG_PATH=C:\path\to\ffmpeg.exe
```

## Port conflict

Port 11122 is used. Kill the existing process:
```powershell
Get-NetTCPConnection -LocalPort 11122 | Stop-Process -Id $_.OwningProcess
```
