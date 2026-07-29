"""Tests for FFmpeg filter builders."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from vfx_mcp.services.ffmpeg_effects import (
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


def test_build_color_grade():
    cmd = build_color_grade("in.mp4", "out.mp4", "sepia")
    assert cmd[0] == "ffmpeg"
    assert "-i" in cmd
    assert "in.mp4" in cmd
    assert "out.mp4" in cmd


def test_build_transition_crossfade():
    cmd = build_transition("a.mp4", "b.mp4", "out.mp4", "crossfade", 1)
    assert "crossfade" in " ".join(cmd)


def test_build_chroma_key():
    cmd = build_chroma_key("in.mp4", "out.mp4", "green", 0.5)
    assert "colorkey" in " ".join(cmd)


def test_build_overlay_text():
    cmd = build_overlay_text("in.mp4", "out.mp4", "Hello", "center", 24)
    assert "drawtext" in " ".join(cmd)


def test_build_overlay_image():
    cmd = build_overlay_image("in.mp4", "logo.png", "out.mp4", "bottom_right", 1.0)
    assert "overlay" in " ".join(cmd)


def test_build_blur():
    cmd = build_blur("in.mp4", "out.mp4", "gaussian", 5)
    assert "gblur" in " ".join(cmd)


def test_build_blur_box():
    cmd = build_blur("in.mp4", "out.mp4", "box", 5)
    assert "boxblur" in " ".join(cmd)


def test_build_speed():
    cmd = build_speed("in.mp4", "out.mp4", 2.0)
    assert "setpts" in " ".join(cmd)


def test_build_crop():
    cmd = build_crop("in.mp4", "out.mp4", 640, 480, 0, 0)
    assert "crop=640:480:0:0" in " ".join(cmd)


def test_build_concat():
    cmd = build_concat(["a.mp4", "b.mp4"], "out.mp4")
    assert cmd[0] == "ffmpeg"


def test_build_concat_empty():
    cmd = build_concat(["a.mp4"], "out.mp4")
    assert cmd[0] == "ffmpeg"
