from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://iktomi:iktomi@0.0.0.0:5433/iktomi"
    SENTRY_DSN: str = "https://45aeefc05e1ff2e0761c623fd3135a7e@o4508111514042368.ingest.de.sentry.io/4508111517646928"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
