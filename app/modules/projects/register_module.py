from fastapi import FastAPI
from sqlalchemy.orm import registry

from app import engine
from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


def register_module(
    app: FastAPI,
    mappers: registry,
    bus: MessageBus,
) -> Container:
    container = Container(engine=engine, bus=bus)
    container.wire()

    start_mappers(mappers)
    app.include_router(routes.router)

    return container
