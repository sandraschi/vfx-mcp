"""PyInstaller entry point — dual transport.

MCP_PORT env var -> HTTP (uvicorn), fallback -> stdio.
"""
import os
import sys

sys.path.insert(0, "src")

port = os.environ.get("MCP_PORT") or os.environ.get("PORT")
if port:
    import uvicorn
    host = os.environ.get("MCP_HOST", "127.0.0.1")
    sys.argv = ["run_server.py", "--mode", "http", "--host", host, "--port", str(port)]

from vfx_mcp.server import app, mcp

if port:
    uvicorn.run(app, host=host, port=int(port), log_level="info")
else:
    import asyncio
    asyncio.run(mcp.run_stdio_async(show_banner=False))
