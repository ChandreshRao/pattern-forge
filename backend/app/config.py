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
    jwt_secret: str = "dev-patternforge-change-me-32b-min!!"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 72


@lru_cache
def get_settings() -> Settings:
    return Settings()
