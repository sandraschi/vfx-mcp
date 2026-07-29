# Tools

## vfx_apply (portmanteau)

Single tool with 9 operations via `operation` parameter.

### Operations

| Operation | Description |
|-----------|-------------|
| color_grade | Sepia, vintage, neon, bleach_bypass, cold, warm, grayscale |
| transition | Crossfade, fade_to_black, wipe_left, wipe_right, slide |
| chroma_key | Green or blue screen removal |
| overlay_text | Text with position and font size |
| overlay_image | Logo/watermark with position and scale |
| blur | Gaussian or box blur (strength 1-20) |
| speed | 0.25x to 4x playback speed |
| crop | Region crop with x/y offset |
| concat | Join 2+ clips via concat demuxer |

## Return Format

```json
{"success": true, "message": "Done", "data": {}, "output_path": "out.mp4"}
```
