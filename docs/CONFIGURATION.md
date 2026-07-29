# Configuration

Environment variables (prefix `VFX_MCP_`):

| Variable | Default | Description |
|----------|---------|-------------|
| VFX_MCP_HOST | 127.0.0.1 | HTTP bind address |
| VFX_MCP_PORT | 11122 | HTTP server port |
| VFX_MCP_FFMPEG_PATH | ffmpeg | FFmpeg binary path |
| VFX_MCP_FFPROBE_PATH | ffprobe | FFprobe binary path |
| VFX_MCP_TIMEOUT_SECONDS | 300 | FFmpeg subprocess timeout |

Copy `.env.example` to `.env` and edit.
