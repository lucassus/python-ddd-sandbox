from dependency_injector import providers
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import async_engine, engine
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.containers import Container
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.shared.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        engine=providers.Object(engine),
        async_engine=providers.Object(async_engine),
        bus=providers.Object(bus),
    )

    container.password_hasher.override(
        providers.Factory(PasswordHasher),
    )

    container.wire(
        [
            ".entrypoints.dependencies",
            ".entrypoints.routes",
        ]
    )

    return container


def bootstrap_accounts_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)

    container = _create_container(bus)
    container.register_command_handlers()
    container.register_event_handlers()

    return container
