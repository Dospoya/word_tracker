from typing import ClassVar

from pydantic import EmailStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Word Tracker"

    database_url: str = "DATABASE_URL"

    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_db: str = "db_name"

    bot_token: str = "TOKEN"
    openai_api_key: str = "OPENAI_API_KEY"
    secret: str = "secret_test"
    api_url: str = "http://localhost:8000"
    api_bot_token: str = "API_TOKEN_BOT"
    first_superuser_email: EmailStr = ""
    first_superuser_password: str = ""
    first_superuser_tg_id: PositiveInt = 1
    first_superuser_first_name: str = ""
    first_superuser_last_name: str = ""
    first_superuser_phone: str = ""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )


settings = Settings()
