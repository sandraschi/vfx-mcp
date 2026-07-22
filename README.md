# vfx-mcp

FastMCP 3.4+ server that wraps FFmpeg for video effects processing. Translates natural language effect descriptions into FFmpeg filter complex strings and runs them via subprocess.

## Features

- **9 effects** via a single `vfx_apply` portmanteau tool: color grading, transitions, chroma key, text overlay, image overlay, blur, speed change, crop, concat
- **Dual transport**: stdio (Claude Desktop / Cursor) and HTTP (FastAPI + MCP streamable)
- **Health & diagnostics endpoints**: `GET /api/health`, `GET /api/v1/diagnostics`

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [FFmpeg](https://ffmpeg.org/) on PATH

## Quick Start

```powershell
uv sync
uv run python -m vfx_mcp --stdio
```

## Usage

### MCP Tools

| Operation | Description |
|-----------|-------------|
| `color_grade` | Apply color grading (sepia, vintage, neon, bleach_bypass, cold, warm, grayscale) |
| `transition` | Crossfade, fade to black, wipe left/right, slide between clips |
| `chroma_key` | Green/blue screen removal |
| `overlay_text` | Add text overlay with position and font size |
| `overlay_image` | Add logo/watermark overlay |
| `blur` | Gaussian or box blur |
| `speed` | Change playback speed (0.25x-4x) |
| `crop` | Crop video to region |
| `concat` | Join multiple clips |

### Ports

| Port | Service |
|------|---------|
| 11122 | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 11123 | Frontend (reserved) |

## Configuration

See `.env.example` for all settings. Key env vars:

| Variable | Default | Description |
|----------|---------|-------------|
| `VFX_MCP_HOST` | `127.0.0.1` | Bind address |
| `VFX_MCP_PORT` | `11122` | HTTP server port |
| `VFX_MCP_FFMPEG_PATH` | `ffmpeg` | FFmpeg binary path |
| `VFX_MCP_TIMEOUT_SECONDS` | `300` | FFmpeg process timeout |
