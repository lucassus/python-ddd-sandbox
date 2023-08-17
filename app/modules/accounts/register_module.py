from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app import engine
from app.modules.shared_kernel.message_bus import MessageBus


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> None:
    from app.modules.accounts.entrypoints import routes
    from app.modules.accounts.entrypoints.containers import Container
    from app.modules.accounts.infrastructure.mappers import start_mappers

    container = Container(
        engine=engine,
        jwt_secret_key="some secret",  # TODO: Take it from the proper config
        bus=providers.Object(bus),
    )
    container.wire()

    start_mappers(mappers)
    app.include_router(routes.router)
