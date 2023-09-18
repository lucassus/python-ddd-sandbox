from dependency_injector import containers, providers
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.db import AppSession
from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.commands import (
    RegisterUser,
    ChangeUserEmailAddress,
    RegisterUserHandler,
    ChangeUserEmailAddressHandler,
)
from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=AsyncEngine)

    get_user_handler = providers.Singleton(GetUserQueryHandler, engine)


class Container(containers.DeclarativeContainer):
    jwt_secret_key = providers.Dependency(instance_of=str)
    engine = providers.Dependency(instance_of=Engine)
    async_engine = providers.Dependency(instance_of=AsyncEngine)
    bus = providers.Dependency(instance_of=MessageBus)

    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(
        UnitOfWork,
        bus,
        session_factory=session_factory.provider,
    )

    auth_token = providers.Singleton(JWTAuthentication, secret_key=jwt_secret_key)
    password_hasher = providers.AbstractFactory(AbstractPasswordHasher)
    authentication = providers.Singleton(Authentication, uow, auth_token, password_hasher)

    queries = providers.Container(QueriesContainer, engine=async_engine)

    register_command_handlers = providers.Callable(
        lambda bus, command_handlers: bus.register_all(command_handlers),
        bus=bus,
        command_handlers=providers.Dict(
            {
                RegisterUser: providers.Factory(RegisterUserHandler, uow, password_hasher),
                ChangeUserEmailAddress: providers.Factory(ChangeUserEmailAddressHandler, uow),
            }
        ),
    )
