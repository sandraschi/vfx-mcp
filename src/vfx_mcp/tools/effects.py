"""VFX portmanteau tool — apply FFmpeg video effects."""

from __future__ import annotations

from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from vfx_mcp.services.ffmpeg_effects import (
    _run_ffmpeg,
    build_blur,
    build_chroma_key,
    build_color_grade,
    build_concat,
    build_crop,
    build_overlay_image,
    build_overlay_text,
    build_speed,
    build_transition,
)


def register_vfx_tools(mcp: FastMCP) -> None:
    @mcp.tool(annotations={"readonly": False})
    def vfx_apply(
        operation: Annotated[
            Literal[
                "color_grade",
                "transition",
                "chroma_key",
                "overlay_text",
                "overlay_image",
                "blur",
                "speed",
                "crop",
                "concat",
            ],
            Field(description="The video effect operation to apply."),
        ],
        input_path: Annotated[str | None, Field(description="Path to input video file.")] = None,
        input_a: Annotated[str | None, Field(description="First input clip (for transition).")] = None,
        input_b: Annotated[str | None, Field(description="Second input clip (for transition).")] = None,
        sources: Annotated[list[str] | None, Field(description="List of source paths (for concat).")] = None,
        overlay_path: Annotated[str | None, Field(description="Path to overlay image (for overlay_image).")] = None,
        output_path: Annotated[str, Field(description="Path for the output video file.")] = "",
        style: Annotated[
            str | None,
            Field(description="Color grade style: sepia, vintage, neon, bleach_bypass, cold, warm, grayscale."),
        ] = None,
        transition: Annotated[
            str | None,
            Field(description="Transition type: crossfade, fade_to_black, wipe_left, wipe_right, slide."),
        ] = None,
        duration: Annotated[int | None, Field(description="Transition duration in seconds (for transition).")] = 1,
        color: Annotated[
            str | None,
            Field(description="Chroma key color: green or blue (for chroma_key)."),
        ] = "green",
        threshold: Annotated[
            float | None,
            Field(description="Chroma key threshold 0.1-1.0 (for chroma_key).", ge=0.1, le=1.0),
        ] = 0.5,
        text: Annotated[str | None, Field(description="Text to overlay (for overlay_text).")] = None,
        position: Annotated[
            str | None,
            Field(
                description=(
                    "Text/image position: top_left, center, bottom_right,"
                    " top_right, bottom_left (for overlay_text, overlay_image)."
                ),
            ),
        ] = "bottom_right",
        font_size: Annotated[int | None, Field(description="Font size for overlay text (for overlay_text).")] = 24,
        scale: Annotated[
            float | None,
            Field(description="Overlay image scale factor (for overlay_image).", ge=0.1, le=5.0),
        ] = 1.0,
        blur_type: Annotated[
            str | None,
            Field(description="Blur type: gaussian or box (for blur)."),
        ] = "gaussian",
        strength: Annotated[
            int | None,
            Field(description="Blur strength 1-20 (for blur).", ge=1, le=20),
        ] = 5,
        rate: Annotated[
            float | None,
            Field(description="Playback speed multiplier 0.25-4.0 (for speed).", ge=0.25, le=4.0),
        ] = 1.0,
        width: Annotated[int | None, Field(description="Crop width in pixels (for crop).")] = None,
        height: Annotated[int | None, Field(description="Crop height in pixels (for crop).")] = None,
        x: Annotated[int | None, Field(description="Crop x offset (for crop).")] = 0,
        y: Annotated[int | None, Field(description="Crop y offset (for crop).")] = 0,
    ) -> dict:
        """Apply a video effect operation via FFmpeg.

        Translates natural language effect descriptions into FFmpeg filter
        complex strings and runs them via subprocess.

        [RATIONALE] Portmanteau pattern groups all video effects under one
        tool with an operation discriminator. This keeps the tool surface
        compact while providing 9 distinct video processing capabilities.

        ## Return Format
        {"success": bool, "message": str, "output_path": str}

        ## Examples
        vfx_apply(operation="color_grade", input_path="in.mp4", output_path="out.mp4", style="sepia")
        vfx_apply(operation="blur", input_path="in.mp4", output_path="out.mp4", blur_type="gaussian", strength=10)
        vfx_apply(operation="concat", sources=["clip1.mp4", "clip2.mp4"], output_path="joined.mp4")
        vfx_apply(operation="speed", input_path="in.mp4", output_path="fast.mp4", rate=2.0)
        """
        cmd = None
        out = output_path or f"vfx_output_{operation}_{hash(input_path or '')}.mp4"

        if operation == "color_grade":
            if not input_path or not style:
                return {"success": False, "message": "input_path and style required for color_grade", "data": {}}
            cmd = build_color_grade(input_path, out, style)

        elif operation == "transition":
            if not input_a or not input_b:
                return {"success": False, "message": "input_a and input_b required for transition", "data": {}}
            cmd = build_transition(input_a, input_b, out, transition or "crossfade", duration or 1)

        elif operation == "chroma_key":
            if not input_path:
                return {"success": False, "message": "input_path required for chroma_key", "data": {}}
            cmd = build_chroma_key(input_path, out, color or "green", threshold or 0.5)

        elif operation == "overlay_text":
            if not input_path or not text:
                return {"success": False, "message": "input_path and text required for overlay_text", "data": {}}
            cmd = build_overlay_text(input_path, out, text, position or "bottom_right", font_size or 24)

        elif operation == "overlay_image":
            if not input_path or not overlay_path:
                return {
                    "success": False,
                    "message": "input_path and overlay_path required for overlay_image",
                    "data": {},
                }
            cmd = build_overlay_image(input_path, overlay_path, out, position or "bottom_right", scale or 1.0)

        elif operation == "blur":
            if not input_path:
                return {"success": False, "message": "input_path required for blur", "data": {}}
            cmd = build_blur(input_path, out, blur_type or "gaussian", strength or 5)

        elif operation == "speed":
            if not input_path:
                return {"success": False, "message": "input_path required for speed", "data": {}}
            cmd = build_speed(input_path, out, rate or 1.0)

        elif operation == "crop":
            if not input_path or not width or not height:
                return {"success": False, "message": "input_path, width, and height required for crop", "data": {}}
            cmd = build_crop(input_path, out, width, height, x or 0, y or 0)

        elif operation == "concat":
            if not sources or len(sources) < 2:
                return {"success": False, "message": "At least 2 source paths required for concat", "data": {}}
            cmd = build_concat(sources, out)

        if not cmd:
            return {"success": False, "message": f"Unknown operation: {operation}", "data": {}}

        result = _run_ffmpeg(cmd)
        result["output_path"] = out
        return result
