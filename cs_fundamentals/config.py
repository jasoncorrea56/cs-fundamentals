from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CS Fundamentals API"
    env: str = "prod"
    port: int = 8080
    log_level: str = "INFO"
    db_url: str | None = None
    web_concurrency: int | None = None
    graceful_timeout: int | None = None

    model_config = SettingsConfigDict(env_file=(".env",), env_file_encoding="utf-8", extra="ignore")


settings = Settings()
