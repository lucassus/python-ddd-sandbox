from dependency_injector import providers
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import async_engine, engine
from app.modules.accounts.infrastructure.containers import Container, AdaptersContainer
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        adapters=AdaptersContainer(
            engine=providers.Object(engine),
            bus=providers.Object(bus),
            jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        ),
        async_engine=providers.Object(async_engine),
    )

    container.wire(
        [
            ".entrypoints.dependencies",
            ".entrypoints.routes",
        ]
    )

    container.register_command_handlers()
    container.register_event_handlers()

    return container


def bootstrap_accounts_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)
    return _create_container(bus)
