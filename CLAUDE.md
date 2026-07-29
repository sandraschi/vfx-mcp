# vfx-mcp — Agent Instructions

## Entry points
- `src/vfx_mcp/server.py` — FastMCP + FastAPI setup
- `src/vfx_mcp/tools/effects.py` — `vfx_apply` portmanteau (9 ops)
- `src/vfx_mcp/services/ffmpeg_effects.py` — FFmpeg filter builders
- `src/vfx_mcp/__main__.py` — CLI entry (--stdio / --serve)

## Standards
- Python: ruff, uv, FastMCP >=3.4.4
- Port: 11122 (backend API + MCP /mcp)
- No webapp (backend-only server)

## Commands
```powershell
uv sync
uv run python -m vfx_mcp --stdio
uv run python -m vfx_mcp --serve
uv run pytest
ruff check src/
ruff format src/
```
