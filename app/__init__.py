from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables
from app.modules import create_app as create_api_app
from app.shared.message_bus import MessageBus


def create_app(bus: MessageBus | None = None):
    if bus is None:
        bus = MessageBus()

    create_tables(engine)

    app = FastAPI()

    app.mount("/api", create_api_app(registry(), bus))

    @app.get("/health")
    def health_endpoint():
        return {"message": "I'm fine!"}

    return app
