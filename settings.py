from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        case_sensitive=False,
        extra="allow",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )
    PG_URL: str
    PG_USER: str
    PG_PASS: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int



settings = Settings()