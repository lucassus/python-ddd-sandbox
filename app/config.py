import os

from pydantic import BaseSettings

database_path = os.path.join(os.path.dirname(__file__), "../db/development.db")


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{database_path}"


settings = Settings()
