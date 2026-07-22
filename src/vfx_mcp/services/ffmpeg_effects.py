"""FFmpeg filter complex builders for video effects."""

from __future__ import annotations

import os
import subprocess

from vfx_mcp.config import load_settings


def build_color_grade(input_path: str, output_path: str, style: str) -> list[str]:
    filters = {
        "sepia": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131",
        "grayscale": "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3",
        "vintage": "curves=vintage",
        "neon": "eq=saturation=3:brightness=0.1:contrast=2",
        "cold": "colorchannelmixer=1.5:0:0:0:0:1.5:0:0:0:0:1.5:0:0:0:0:1",
        "warm": "colorchannelmixer=1.2:0:0:0:0:1:0:0:0:0:0.8",
        "bleach_bypass": (
            "colorchannelmixer=1.2:0:0:0:0:1.2:0:0:0:0:1.2:0:0:0:0:1,eq=saturation=0.5:brightness=0.05:contrast=1.3"
        ),
    }
    f = filters.get(style, "")
    cfg = load_settings()
    cmd = [cfg.ffmpeg_path, "-i", input_path, "-vf", f, "-c:a", "copy", output_path, "-y"]
    return cmd


def build_transition(input_a: str, input_b: str, output_path: str, transition: str, duration: int) -> list[str]:
    cfg = load_settings()
    if transition == "crossfade":
        cmd = [
            cfg.ffmpeg_path,
            "-i",
            input_a,
            "-i",
            input_b,
            "-filter_complex",
            f"crossfade=d={duration}",
            output_path,
            "-y",
        ]
    elif transition == "fade_to_black":
        cmd = [
            cfg.ffmpeg_path,
            "-i",
            input_a,
            "-filter_complex",
            f"fade=t=out:st=0:d={duration}",
            "-i",
            input_b,
            "-filter_complex",
            f"fade=t=in:st=0:d={duration}",
            "-filter_complex",
            "concat=n=2:v=1:a=1",
            output_path,
            "-y",
        ]
    elif transition in ("wipe_left", "wipe_right"):
        direction = "from_left" if transition == "wipe_right" else "from_right"
        cmd = [
            cfg.ffmpeg_path,
            "-i",
            input_a,
            "-i",
            input_b,
            "-filter_complex",
            f"xfade=transition=wipe{direction}:duration={duration}",
            output_path,
            "-y",
        ]
    elif transition == "slide":
        cmd = [
            cfg.ffmpeg_path,
            "-i",
            input_a,
            "-i",
            input_b,
            "-filter_complex",
            f"xfade=transition=slideright:duration={duration}",
            output_path,
            "-y",
        ]
    else:
        cmd = [cfg.ffmpeg_path, "-i", input_a, "-i", input_b, "-c", "copy", output_path, "-y"]
    return cmd


def build_chroma_key(input_path: str, output_path: str, color: str, threshold: float) -> list[str]:
    color_val = "0x00FF00" if color == "green" else "0x0000FF"
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        f"colorkey={color_val}:{threshold}:0.1:1",
        "-c:a",
        "copy",
        output_path,
        "-y",
    ]
    return cmd


def build_overlay_text(input_path: str, output_path: str, text: str, position: str, font_size: int) -> list[str]:
    pos_map = {
        "top_left": "x=10:y=10",
        "center": "x=(w-text_w)/2:y=(h-text_h)/2",
        "bottom_right": "x=w-tw-10:y=h-th-10",
    }
    pos = pos_map.get(position, "x=10:y=10")
    escaped = text.replace("'", "'\\\\''")
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        f"drawtext=text='{escaped}':fontsize={font_size}:fontcolor=white:{pos}",
        "-c:a",
        "copy",
        output_path,
        "-y",
    ]
    return cmd


def build_overlay_image(input_path: str, overlay_path: str, output_path: str, position: str, scale: float) -> list[str]:
    pos_map = {
        "top_left": "10:10",
        "top_right": "W-w-10:10",
        "center": "(W-w)/2:(H-h)/2",
        "bottom_left": "10:H-h-10",
        "bottom_right": "W-w-10:H-h-10",
    }
    pos = pos_map.get(position, "W-w-10:H-h-10")
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-i",
        overlay_path,
        "-filter_complex",
        f"[1]scale=iw*{scale}:ih*{scale}[ovr];[0][ovr]overlay={pos}",
        "-c:a",
        "copy",
        output_path,
        "-y",
    ]
    return cmd


def build_blur(input_path: str, output_path: str, blur_type: str, strength: int) -> list[str]:
    if blur_type == "gaussian":
        filter_str = f"gblur=sigma={strength}"
    else:
        filter_str = f"boxblur=luma_radius={strength}:luma_power=1"
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        filter_str,
        "-c:a",
        "copy",
        output_path,
        "-y",
    ]
    return cmd


def build_speed(input_path: str, output_path: str, rate: float) -> list[str]:
    setpts = f"setpts={1 / rate:.4f}*PTS"
    atempo = min(max(rate, 0.5), 100.0)
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        setpts,
        "-af",
        f"atempo={atempo}",
        output_path,
        "-y",
    ]
    return cmd


def build_crop(input_path: str, output_path: str, width: int, height: int, x: int, y: int) -> list[str]:
    cfg = load_settings()
    cmd = [
        cfg.ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        f"crop={width}:{height}:{x}:{y}",
        "-c:a",
        "copy",
        output_path,
        "-y",
    ]
    return cmd


def build_concat(sources: list[str], output_path: str) -> list[str]:
    cfg = load_settings()
    list_path = None
    try:
        import tempfile

        fd, list_path = tempfile.mkstemp(suffix=".txt", prefix="vfx_concat_")
        with os.fdopen(fd, "w") as f:
            for src in sources:
                abs_src = os.path.abspath(src)
                f.write(f"file '{abs_src}'\n")
        cmd = [
            cfg.ffmpeg_path,
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_path,
            "-c",
            "copy",
            output_path,
            "-y",
        ]
        return cmd
    except Exception:
        from functools import reduce

        cmd = reduce(lambda acc, s: [*acc, "-i", s], sources, [cfg.ffmpeg_path])
        cmd += ["-filter_complex", f"concat=n={len(sources)}:v=1:a=1", output_path, "-y"]
        return cmd


def _run_ffmpeg(cmd: list[str], timeout: int = 300) -> dict:
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)  # noqa: S603
        if r.returncode != 0:
            return {"success": False, "message": r.stderr.decode()[:500]}
        return {"success": True, "message": "Done"}
    except subprocess.TimeoutExpired:
        return {"success": False, "message": "FFmpeg timed out"}
    except FileNotFoundError:
        return {"success": False, "message": "FFmpeg not found on PATH"}
