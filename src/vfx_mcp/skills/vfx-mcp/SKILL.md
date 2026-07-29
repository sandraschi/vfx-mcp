# vfx-mcp Skill

## What it does

FastMCP 3.4+ server wrapping FFmpeg for video effects processing. Translates natural language effect descriptions into FFmpeg filter complex strings and runs them via subprocess.

## Tools

### vfx_apply (portmanteau)

| Operation | Description | Required Params |
|-----------|-------------|----------------|
| color_grade | Apply color grading (sepia, vintage, neon, bleach_bypass, cold, warm, grayscale) | input_path, output_path, style |
| transition | Crossfade, fade_to_black, wipe_left, wipe_right, slide | input_a, input_b, output_path |
| chroma_key | Green/blue screen removal | input_path, output_path |
| overlay_text | Add text overlay | input_path, output_path, text |
| overlay_image | Add logo/watermark overlay | input_path, overlay_path, output_path |
| blur | Gaussian or box blur | input_path, output_path |
| speed | Change playback speed (0.25x-4x) | input_path, output_path, rate |
| crop | Crop video to region | input_path, output_path, width, height |
| concat | Join multiple clips | sources (list), output_path |

## Return Format

```json
{"success": true, "message": "Done", "data": {...}, "output_path": "..."}
```

## Configuration

- `VFX_MCP_PORT` (default: 11122)
- `VFX_MCP_FFMPEG_PATH` (default: ffmpeg)
- `VFX_MCP_TIMEOUT_SECONDS` (default: 300)
