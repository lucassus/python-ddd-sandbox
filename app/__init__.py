from fastapi import FastAPI

from app.command import create_app as create_commands_app
from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables


def create_app():
    create_tables(engine)

    app = FastAPI()

    app.mount("/commands", create_commands_app())

    @app.get("/health")
    def health_endpoint():
        return {"message": "I'm fine!"}

    return app
