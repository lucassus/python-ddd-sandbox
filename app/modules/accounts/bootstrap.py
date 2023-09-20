from dependency_injector import providers
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import async_engine, engine
from app.modules.accounts.application.containers import AppContainer
from app.modules.accounts.infrastructure.containers import AdaptersContainer, QueriesContainer
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.authentication_contract import AuthenticationContract
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

    return container


def _create_queries_container() -> QueriesContainer:
    container = QueriesContainer(
        engine=providers.Object(async_engine),
    )

    container.wire(modules=[".entrypoints.routes"])

    return container


def bootstrap_accounts_module(mappers: registry, bus: MessageBus) -> AuthenticationContract:
    start_mappers(mappers)

    container = _create_commands_container(bus)

    bus.register_all(container.command_handlers())
    bus.listen_all(container.event_handlers())

    _create_queries_container()

    return container.authentication()
