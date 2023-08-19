from dependency_injector import containers, providers
from sqlalchemy import Engine

from app.infrastructure.db import AppSession, engine
from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.shared_kernel.message_bus import MessageBus


class ApplicationContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    bus = providers.Dependency(instance_of=MessageBus)

    jwt_secret_key = providers.Dependency(instance_of=str)
    jwt = providers.Singleton(JWT, secret_key=jwt_secret_key)

    session_factory = providers.Factory(AppSession, bind=engine)
    uow = providers.Singleton(UnitOfWork, session_factory=session_factory.provider)

    register_user = providers.Singleton(RegisterUser, uow=uow, bus=bus)
    authentication = providers.Singleton(Authentication, uow=uow, jwt=jwt)
    change_user_email_address = providers.Singleton(ChangeUserEmailAddress, uow=uow)


class QueriesContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    get_user = providers.Singleton(GetUserQuery, engine=engine)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".dependencies",
            ".routes",
        ]
    )

    engine = providers.Object(engine)

    bus = providers.Dependency(instance_of=MessageBus)
    jwt_secret_key = providers.Dependency(instance_of=str)

    application = providers.Container(
        ApplicationContainer,
        jwt_secret_key=jwt_secret_key,
        bus=bus,
        engine=engine,
    )

    queries = providers.Container(QueriesContainer, engine=engine)
