from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.infrastructure.db import engine
from app.modules.accounts.containers import Container
from app.modules.accounts.entrypoints import routes
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object("asdf"),  # TODO: Fix me
        bus=providers.Object(bus),
        engine=providers.Object(engine),
    )

    container.commands.uow.override(
        providers.Factory(
            UnitOfWork,
            session_factory=container.infrastructure.session_factory(),
        )
    )

    container.wire(
        modules=[
            ".entrypoints.dependencies",
            ".entrypoints.routes",
        ]
    )

    start_mappers(mappers)
    app.include_router(routes.router)

    return container
