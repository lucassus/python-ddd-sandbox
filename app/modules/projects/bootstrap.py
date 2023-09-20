from dependency_injector import providers
from sqlalchemy.orm import registry

from app.infrastructure.db import async_engine, engine
from app.modules.authentication_contract import AuthenticationContract
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus, authentication: AuthenticationContract) -> Container:
    container = Container(
        engine=engine,
        async_engine=async_engine,
        bus=bus,
    )

    container.authentication.override(providers.Factory(lambda: authentication))

    container.wire(
        modules=[
            ".application.event_handlers",
            ".entrypoints.dependencies",
        ],
        packages=[".entrypoints.routes"],
    )

    return container


def bootstrap_projects_module(
    mappers: registry,
    bus: MessageBus,
    authentication: AuthenticationContract,
):
    start_mappers(mappers)

    container = _create_container(bus, authentication)

    bus.register_all(container.command_handlers())
    bus.listen_all(container.event_handlers())
