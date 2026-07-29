# Development

## Setup

```powershell
uv sync
```

## Run

```powershell
# stdio mode (Claude Desktop / Cursor)
uv run python -m vfx_mcp --stdio

# HTTP mode
uv run python -m vfx_mcp --serve
```

## Lint

```powershell
ruff check src/
ruff format src/
```

## Test

```powershell
uv run pytest
```
