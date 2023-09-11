from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession
from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.queries import GetUserQueryHandler
from app.shared.message_bus import MessageBus


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    get_user = providers.Singleton(GetUserQueryHandler, engine=engine)


class Container(containers.DeclarativeContainer):
    jwt_secret_key = providers.Dependency(instance_of=str)
    engine = providers.Dependency(instance_of=Engine)
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

    queries = providers.Container(QueriesContainer, engine=engine)
