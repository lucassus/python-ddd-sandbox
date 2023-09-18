from dependency_injector import containers, providers
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from app.infrastructure.db import AppSession
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
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
