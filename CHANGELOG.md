# Changelog

## 0.1.0 (2026-07-30)

- Initial release
- `vfx_apply` portmanteau tool (9 effects: color_grade, transition, chroma_key, overlay_text, overlay_image, blur, speed, crop, concat)
- Dual transport: stdio (--stdio) and HTTP (--serve)
- FastAPI health endpoint: GET /api/health
- Diagnostics endpoint: GET /api/v1/diagnostics
- CORS with Tailscale + Tauri support
