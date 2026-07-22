"""Tool registration for vfx-mcp."""

from __future__ import annotations

from fastmcp import FastMCP


def register_all_tools(mcp: FastMCP) -> None:
    from vfx_mcp.tools.effects import register_vfx_tools

    register_vfx_tools(mcp)
