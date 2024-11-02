from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class StorageConfig(BaseModel):
    base: str
    throttling: str


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False


class MovieConfig(BaseModel):
    url: str
    token: str


class WeatherConfig(BaseModel):
    url: str
    token: str


class BotConfig(BaseModel):
    token: str
    admin_id: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    db: DatabaseConfig
    movie: MovieConfig
    weather: WeatherConfig
    bot: BotConfig
    storage: StorageConfig


settings = Settings()
