# AGENTS.md — vfx-mcp

## Project Identity
- **Name**: vfx-mcp
- **Purpose**: FFmpeg video effects processing — color grading, transitions, chroma key, blur, speed, crop, concat, text/image overlay
- **Stack**: FastMCP 3.4+, FastAPI, Starlette
- **Port**: 11122 (backend + MCP HTTP), 11123 (frontend, reserved)
- **Transports**: stdio (`--stdio`) and streamable HTTP (`--serve`)

## Key Files

| File | Purpose |
|------|---------|
| `src/vfx_mcp/server.py` | FastMCP + FastAPI setup, health endpoints |
| `src/vfx_mcp/tools/effects.py` | `vfx_apply` portmanteau tool (9 operations) |
| `src/vfx_mcp/services/ffmpeg_effects.py` | FFmpeg filter complex builders |
| `src/vfx_mcp/config.py` | Settings via env (prefix `VFX_MCP_`) |

## Testing

```powershell
uv run pytest
```

## Linting

```powershell
ruff check src/
ruff format src/
```
