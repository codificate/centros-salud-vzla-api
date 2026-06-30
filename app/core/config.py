import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

load_dotenv()

_DEFAULT_CREDENTIALS_PATH: Final[Path] = Path(__file__).parent / "serviceAccount.json"


class Settings:
    """Application settings loaded from OS environment variables."""

    def __init__(self) -> None:
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Vercel + FastAPI")
        self.VERSION: str = os.getenv("VERSION", "1.0.0")
        self.API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")

        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

        credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        credentials_json = os.getenv("FIREBASE_CREDENTIALS")

        if self.ENVIRONMENT == "development" and not credentials_path:
            if _DEFAULT_CREDENTIALS_PATH.is_file():
                credentials_path = str(_DEFAULT_CREDENTIALS_PATH)

        self.FIREBASE_CREDENTIALS_PATH: str | None = credentials_path
        self.FIREBASE_CREDENTIALS: str | None = credentials_json
        self.FIREBASE_PROJECT_ID: str | None = os.getenv("FIREBASE_PROJECT_ID")
        self.FIREBASE_STORAGE_BUCKET: str | None = os.getenv("FIREBASE_STORAGE_BUCKET")

    @property
    def is_dev(self) -> bool:
        """True when running in a local/dev environment."""
        return self.ENVIRONMENT.lower().startswith("dev")


settings = Settings()
