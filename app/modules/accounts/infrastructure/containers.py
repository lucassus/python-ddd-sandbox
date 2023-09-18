from dependency_injector import containers, providers
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.db import AppSession
from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.commands import (
    ChangeUserEmailAddress,
    ChangeUserEmailAddressHandler,
    RegisterUser,
    RegisterUserHandler,
)
from app.modules.accounts.application.event_handlers import SendWelcomeEmail
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import MessageBus


class AdaptersContainer(containers.DeclarativeContainer):
    bus = providers.Dependency(instance_of=MessageBus)
    engine = providers.Dependency(instance_of=Engine)

    uow = providers.Singleton(
        UnitOfWork,
        bus,
        session_factory=providers.Factory(AppSession, bind=engine).provider,
    )

    jwt_secret_key = providers.Dependency(instance_of=str)
    auth_token = providers.Singleton(JWTAuthentication, secret_key=jwt_secret_key)

    password_hasher = providers.Factory(PasswordHasher)


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=AsyncEngine)
    get_user = providers.Singleton(GetUserQueryHandler, engine)


class Container(containers.DeclarativeContainer):
    adapters = providers.DependenciesContainer()
    bus = adapters.bus

    authentication = providers.Singleton(
        Authentication,
        adapters.uow,
        adapters.auth_token,
        adapters.password_hasher,
    )

    register_command_handlers = providers.Callable(
        lambda bus, command_handlers: bus.register_all(command_handlers),
        bus=adapters.bus,
        command_handlers=providers.Dict(
            {
                RegisterUser: providers.Factory(RegisterUserHandler, adapters.uow, adapters.password_hasher),
                ChangeUserEmailAddress: providers.Factory(ChangeUserEmailAddressHandler, adapters.uow),
            }
        ),
    )

    register_event_handlers = providers.Callable(
        lambda bus, event_handlers: bus.listen_all(event_handlers),
        bus=adapters.bus,
        event_handlers=providers.Dict(
            {
                UserAccountCreated: providers.List(providers.Factory(SendWelcomeEmail, adapters.uow)),
            }
        ),
    )

    async_engine = providers.Dependency(instance_of=AsyncEngine)
    queries = providers.Container(QueriesContainer, engine=async_engine)
