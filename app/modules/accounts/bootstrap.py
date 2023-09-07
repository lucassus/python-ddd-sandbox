from dependency_injector import providers
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import engine
from app.infrastructure.message_bus import MessageBus
from app.modules.accounts.application.commands import (
    ChangeUserEmailAddress,
    ChangeUserEmailAddressHandler,
    RegisterUser,
    RegisterUserHandler,
)
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.mappers import start_mappers


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        engine=providers.Object(engine),
        bus=providers.Object(bus),
    )

    container.application.password_hasher.override(
        providers.Factory(PasswordHasher),
    )

    container.wire(
        [
            ".entrypoints.dependencies",
            ".entrypoints.routes",
        ]
    )

    return container


def _register_commands(bus: MessageBus, container: Container) -> None:
    uow = container.application.uow()

    bus.register(
        RegisterUser,
        RegisterUserHandler(
            uow=uow,
            password_hasher=container.application.password_hasher(),
        ),
    )

    bus.register(ChangeUserEmailAddress, ChangeUserEmailAddressHandler(uow=uow))


def bootstrap_accounts_module(mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)

    container = _create_container(bus)
    _register_commands(bus, container)

    return container
