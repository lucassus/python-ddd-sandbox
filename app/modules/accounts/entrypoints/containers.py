from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.modules.accounts.infrastructure.queries.find_user_query import GetUserSQLQuery
from app.modules.shared_kernel.message_bus import MessageBus


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".dependencies",
            ".routes",
        ],
        auto_wire=False,
    )

    engine = providers.Dependency(instance_of=Engine)
    connection = providers.Resource(init_connection, engine=engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    jwt_secret_key = providers.Dependency(instance_of=str)
    jwt = providers.Factory(JWT, secret_key=jwt_secret_key)

    bus = providers.Dependency(instance_of=MessageBus)
    uow = providers.Singleton(UnitOfWork, session_factory=session_factory)

    register_user = providers.Singleton(RegisterUser, uow=uow, bus=bus)
    authenticate = providers.Factory(Authentication, uow=uow, jwt=jwt)
    change_user_email_address = providers.Singleton(ChangeUserEmailAddress, uow=uow)

    get_user_query = providers.Factory(GetUserSQLQuery, connection=connection)
