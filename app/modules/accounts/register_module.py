from dependency_injector import providers
from fastapi import FastAPI
from sqlalchemy.orm import registry

from app.config import app_config
from app.infrastructure.db import engine
from app.modules.accounts.application.commands.change_user_email_address import (
    ChangeUserEmailAddress,
    ChangeUserEmailAddressHandler,
)
from app.modules.accounts.application.commands.register_user import RegisterUser, RegisterUserHandler
from app.modules.accounts.entrypoints import routes
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.mappers import start_mappers
from app.modules.shared_kernel.message_bus import MessageBus


def _create_container(bus: MessageBus) -> Container:
    container = Container(
        jwt_secret_key=providers.Object(app_config.jwt_secret_key),
        engine=providers.Object(engine),
        bus=providers.Object(bus),
    )

    container.application.password_hasher.override(
        providers.Factory(PasswordHasher),
    )

    container.wire()

    return container


# TODO: Rename this function to bootstrap_module
def register_module(app: FastAPI, mappers: registry, bus: MessageBus) -> Container:
    start_mappers(mappers)
    app.include_router(routes.router)

    container = _create_container(bus)

    bus.register(
        RegisterUser,
        RegisterUserHandler(
            uow=container.application.uow(),
            password_hasher=container.application.password_hasher(),
        ),
    )

    bus.register(
        ChangeUserEmailAddress,
        ChangeUserEmailAddressHandler(
            uow=container.application.uow(),
        ),
    )

    return container
