from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.command.accounts.application.change_user_email_address import ChangeUserEmailAddress
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.infrastructure.adapters.unit_of_work import UnitOfWork
from app.command.accounts.infrastructure.queries.find_user_query import FindUserQuery
from app.command.shared_kernel.message_bus import MessageBus


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".endpoints"],
        auto_wire=False,
    )

    engine = providers.Dependency(instance_of=Engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    bus = providers.Dependency(instance_of=MessageBus)
    uow = providers.Singleton(UnitOfWork, session_factory=session_factory)

    register_user = providers.Singleton(RegisterUser, uow=uow, bus=bus)
    change_user_email_address = providers.Singleton(ChangeUserEmailAddress, uow=uow)

    # Queries

    connection = providers.Resource(init_connection, engine=engine)
    find_user_query = providers.Factory(FindUserQuery, connection=connection)
