from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import engine
from app.modules.accounts.entrypoints import routes
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        engine=providers.Object(engine),
        bus=providers.Object(bus),
    )

    container.wire()

    return container


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)
    app.include_router(routes.router)

    return _create_container(bus)
