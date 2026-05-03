import tempfile
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def default_database_url() -> str:
    return f"sqlite:///{(Path(tempfile.gettempdir()) / 'ToneCraftAI' / 'tonecraft.db').as_posix()}"


class Settings(BaseSettings):
    app_name: str = "ToneCraft AI"
    api_prefix: str = "/api"
    database_url: str = Field(default_factory=default_database_url)
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str | None = None
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
