from fastapi import FastAPI

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables
from app.modules import create_app as create_api_app


def create_app():
    create_tables(engine)

    app = FastAPI()

    app.mount("/api", create_api_app())

    @app.get("/health")
    def health_endpoint():
        return {"message": "I'm fine!"}

    return app
