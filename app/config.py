from pathlib import Path

from pydantic import BaseSettings

database_path = (Path(__file__).parent / "infrastructure/databases/development.db").resolve()


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{database_path}"


settings = Settings()
