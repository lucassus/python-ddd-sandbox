from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.command.shared_kernel.message_bus import MessageBus
from app.infrastructure.db import engine


# TODO: __init__ is hard to find, move it to accounts/register.py
# TODO: ...and do the same for projects
def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> None:
    from app.command.accounts.entrypoints import endpoints
    from app.command.accounts.entrypoints.containers import Container
    from app.command.accounts.infrastructure.mappers import start_mappers

    container = Container(engine=engine, bus=providers.Object(bus))
    container.wire()

    start_mappers(mappers)
    app.include_router(endpoints.router)
