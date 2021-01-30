import os
import sys

from pydantic import BaseSettings

database_path = os.path.join(
    os.path.dirname(__file__),
    "../development.db" if "pytest" not in sys.modules else "../test.db",
)


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{database_path}"


settings = Settings()
