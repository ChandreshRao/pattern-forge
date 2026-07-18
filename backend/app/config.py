from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./patternforge.db"
    content_root: Path = Path(__file__).resolve().parents[2] / "content"
    judge0_base_url: str = "http://localhost:2358"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    campaign_id: str = "detective_academy"


@lru_cache
def get_settings() -> Settings:
    return Settings()
