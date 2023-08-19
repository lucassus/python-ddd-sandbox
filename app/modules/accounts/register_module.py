from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.config import settings
from app.infrastructure.db import engine
from app.modules.accounts.application.containers import Container
from app.modules.accounts.entrypoints import routes
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.containers import InfrastructureContainer
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.accounts.queries.containers import QueriesContainer
from app.modules.shared_kernel.message_bus import MessageBus


def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> Container:
    infrastructure_container = InfrastructureContainer(engine=engine)
    queries_container = QueriesContainer(connection=infrastructure_container.connection())

    container = Container(
        jwt_secret_key=settings.jwt_secret_key,
        bus=providers.Object(bus),
    )

    container.uow.override(
        providers.Factory(
            UnitOfWork,
            session_factory=infrastructure_container.session_factory(),
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
