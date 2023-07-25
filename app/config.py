from pathlib import Path

from pydantic import BaseSettings

# TODO: Fix it
database_path = (Path(__file__).parent / "../db/development.db").resolve()


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{database_path}"


settings = Settings()
