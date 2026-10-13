# Per-repo fleet start config for vfx-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'vfx-mcp'
    BackendPort  = 11122
    FrontendPort = 0
    HealthPath   = '/api/health'
    WebRoot      = '.'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'vfx_mcp.server:app'
        SyncExtras    = @('dev')
        SyncOnStart  = $true
        Env           = @{ WEB_PORT = '11122' }
    }
    Frontend = @{
        Kind = 'none'
    }
}
