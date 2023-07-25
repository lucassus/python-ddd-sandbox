import os
from enum import StrEnum

from pydantic import BaseSettings
from pydantic.fields import Field


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


_environment = os.getenv("APP_ENV", Environment.DEVELOPMENT)


class Settings(BaseSettings):
    environment: Environment = Field(..., env="APP_ENV")
    database_url: str = Field(..., env="APP_DATABASE_URL")

    class Config:
        env_file = f".env.{_environment}"
        env_file_encoding = "utf-8"


settings = Settings()
