from pathlib import Path
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_CREDENTIALS_PATH: Final[Path] = Path(__file__).parent / "serviceAccount.json"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Vercel + FastAPI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    FIREBASE_CREDENTIALS_PATH: str | None = Field(
        default_factory=lambda: str(_DEFAULT_CREDENTIALS_PATH)
        if _DEFAULT_CREDENTIALS_PATH.is_file()
        else None
    )
    FIREBASE_CREDENTIALS: str | None = None
    FIREBASE_PROJECT_ID: str | None = None
    FIREBASE_STORAGE_BUCKET: str | None = None
    ENVIRONMENT: str = "development"

    @property
    def is_dev(self) -> bool:
        """True when running in a local/dev environment."""
        return self.ENVIRONMENT.lower().startswith("dev")


settings = Settings()
