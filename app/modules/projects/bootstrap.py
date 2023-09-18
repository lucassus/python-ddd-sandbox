from sqlalchemy.orm import registry

from app.infrastructure.db import async_engine, engine
from app.modules.projects.infrastructure.containers import Container
from app.modules.projects.infrastructure.mappers import start_mappers
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        engine=engine,
        async_engine=async_engine,
        bus=bus,
    )

    container.wire(
        modules=[
            ".application.event_handlers",
            ".entrypoints.dependencies",
        ],
        packages=[".entrypoints.routes"],
    )

    return container


def bootstrap_projects_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)

    container = _create_container(bus)
    container.register_command_handlers()
    container.register_event_handlers()

    return container
