
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Word Tracker'
    database_url: str = 'DATABASE_URL'
    bot_token: str = 'TOKEN'
    openai_api_key: str = 'OPENAI_API_KEY'
    secret: str = 'secret_test'
    api_url: str = 'http://localhost:8000'
    api_bot_token: str
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None
    first_superuser_tg_id: int | None = None
    first_superuser_first_name: str | None = None
    first_superuser_last_name: str | None = None
    first_superuser_phone: str | None = None

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
