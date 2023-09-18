from dependency_injector import providers
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import async_engine, engine
from app.modules.accounts.infrastructure.containers import AdaptersContainer, QueriesContainer
from app.modules.accounts.application.containers import AppContainer
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.shared.message_bus import MessageBus


def _create_commands_container(bus: MessageBus) -> AppContainer:
    container = AppContainer(
        bus=providers.Object(bus),
        adapters=AdaptersContainer(
            bus=providers.Object(bus),
            engine=providers.Object(engine),
            jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        ),
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


def _create_queries_container() -> QueriesContainer:
    container = QueriesContainer(
        engine=providers.Object(async_engine),
    )

    container.wire(modules=[".entrypoints.routes"])

    return container


def bootstrap_accounts_module(mappers: registry, bus: MessageBus) -> AppContainer:
    start_mappers(mappers)

    _create_queries_container()
    return _create_commands_container(bus)
