"""Runtime configuration for vfx-mcp."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VFX_MCP_",
        env_file=".env",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = 11122
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"
    timeout_seconds: int = 300


def load_settings() -> Settings:
    return Settings()
