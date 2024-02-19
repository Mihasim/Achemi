from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_HOSTNAME: str = "localhost"
    POSTGRESQL_USERNAME: str = "postgres"
    POSTGRESQL_PASSWORD: str = ""
    POSTGRESQL_DATABASE: str = "codeforces tasks"

    TELEGRAM_API_KEI: str = ""


settings = Settings()
