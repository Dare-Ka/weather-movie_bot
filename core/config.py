from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "core/.env",
    )
    BOT_TOKEN: str
    TESTS_BOT_TOKEN: str
    WEATHER_API_KEY: str
    WEATHER_URL: str
    KINOPOISK_BASE_URL: str
    ADMIN_ID: int
    API_KINOPOISK_TOKEN: str
    OTHER_API_KINOPOISK_TOKEN_1: str
    OTHER_API_KINOPOISK_TOKEN_2: str
    OTHER_API_KINOPOISK_TOKEN_3: str
    OTHER_API_KINOPOISK_TOKEN_4: str
    OTHER_API_KINOPOISK_TOKEN_5: str


class DatabaseSettings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=BASE_DIR / "core/.env",
    # )
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/core/tg.db"
    db_echo: bool = True


settings = Settings()

db_settings = DatabaseSettings()

API_KINOPOISK_TOKEN_LIST = [
    settings.API_KINOPOISK_TOKEN,
    settings.OTHER_API_KINOPOISK_TOKEN_1,
    settings.OTHER_API_KINOPOISK_TOKEN_2,
    settings.OTHER_API_KINOPOISK_TOKEN_3,
    settings.OTHER_API_KINOPOISK_TOKEN_4,
    settings.OTHER_API_KINOPOISK_TOKEN_5,
]
