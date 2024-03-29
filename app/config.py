import os
from enum import StrEnum

from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


_environment = os.getenv("APP_ENV", Environment.DEVELOPMENT)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{_environment}",
        env_file_encoding="utf-8",
    )

    environment: Environment = Field(..., validation_alias="APP_ENV")
    database_url: str = Field(..., validation_alias="APP_DATABASE_URL")
    async_database_url: str = Field(..., validation_alias="APP_ASYNC_DATABASE_URL")
    jwt_secret_key: str = Field(..., validation_alias="APP_JWT_SECRET_KEY")


app_config = Settings()
