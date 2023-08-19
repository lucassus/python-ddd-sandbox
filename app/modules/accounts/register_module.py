from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.config import settings
from app.modules.accounts.containers import Container
from app.modules.accounts.entrypoints import routes
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object(settings.jwt_secret_key),
        bus=providers.Object(bus),
    )

    container.commands.uow.override(
        providers.Factory(
            UnitOfWork,
            session_factory=container.infrastructure.session_factory(),  # TODO: Find a bit better option to pass it
        )
    )

    container.wire(
        modules=[
            ".entrypoints.dependencies",
            ".entrypoints.routes",
        ]
    )

    return container


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)
    app.include_router(routes.router)

    return _create_container(bus)
