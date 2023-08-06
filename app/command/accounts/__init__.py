from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.command.shared_kernel.message_bus import MessageBus


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> None:
    from app.command.accounts.entrypoints import endpoints
    from app.command.accounts.entrypoints.containers import Container
    from app.command.accounts.infrastructure.mappers import start_mappers

    container = Container(bus=providers.Object(bus))
    container.wire(modules=[endpoints])

    start_mappers(mappers)
    app.include_router(endpoints.router)
