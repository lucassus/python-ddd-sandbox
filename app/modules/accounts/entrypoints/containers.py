from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession
from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.shared.message_bus import MessageBus


class ApplicationContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    bus = providers.Dependency(instance_of=MessageBus)

    jwt_secret_key = providers.Dependency(instance_of=str)

    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(UnitOfWork, session_factory=session_factory.provider, bus=bus)

    auth_token = providers.Singleton(JWTAuthentication, secret_key=jwt_secret_key)
    password_hasher = providers.AbstractFactory(AbstractPasswordHasher)
    authentication = providers.Singleton(
        Authentication,
        uow=uow,
        token=auth_token,
        password_hasher=password_hasher,
    )


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    get_user = providers.Singleton(GetUserQuery, engine=engine)


class Container(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)

    bus = providers.Dependency(instance_of=MessageBus)
    jwt_secret_key = providers.Dependency(instance_of=str)

    application = providers.Container(
        ApplicationContainer,
        jwt_secret_key=jwt_secret_key,
        bus=bus,
        engine=engine,
    )

    queries = providers.Container(QueriesContainer, engine=engine)
