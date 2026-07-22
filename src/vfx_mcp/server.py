"""FastMCP + FastAPI server with health endpoint and tool registration."""

from __future__ import annotations

import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from vfx_mcp import __version__
from vfx_mcp.config import load_settings
from vfx_mcp.tools import register_all_tools

settings = load_settings()

mcp = FastMCP(
    "vfx-mcp",
    version=__version__,
    instructions=(
        "FFmpeg video effects via MCP — color grading, transitions, chroma key,"
        " blur, speed, crop, concat, text/image overlay."
    ),
)

register_all_tools(mcp)

app = FastAPI(title="vfx-mcp", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{settings.port}",
        f"http://127.0.0.1:{settings.port}",
        "http://tauri.localhost",
        "https://tauri.localhost",
        "tauri://localhost",
    ],
    allow_origin_regex=r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_start_time = time.time()


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "server": "vfx-mcp",
        "version": __version__,
        "uptime_seconds": int(time.time() - _start_time),
        "transport": "http",
    }


@app.get("/api/v1/diagnostics")
async def diagnostics():
    import shutil

    ffmpeg_path = shutil.which(settings.ffmpeg_path)
    tools = await mcp.list_tools()
    return {
        "status": "ok",
        "server": "vfx-mcp",
        "version": __version__,
        "uptime_seconds": int(time.time() - _start_time),
        "tool_count": len(tools),
        "tools": [{"name": t.name} for t in tools],
        "ffmpeg_available": ffmpeg_path is not None,
        "ffmpeg_path": ffmpeg_path,
        "port": settings.port,
        "system": {"windows": os.name == "nt"},
    }


mcp_app = mcp.http_app()
app.mount("/mcp", mcp_app)
