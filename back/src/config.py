from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://iktomi:iktomi@iktomi-postgres:5432/iktomi"
    SENTRY_DSN: str = "https://45aeefc05e1ff2e0761c623fd3135a7e@o4508111514042368.ingest.de.sentry.io/4508111517646928"

    RPC_URL: str = "https://eth-mainnet.g.alchemy.com/v2/<secret>"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    JWT_SECRET: str = "<264 byte str>"
    ISSUER: str = 'https://iktomi.pro'


settings = Settings()
