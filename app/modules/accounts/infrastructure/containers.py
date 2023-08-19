from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.modules.accounts.infrastructure.queries.find_user_query import GetUserSQLQuery


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class InfrastructureContainer(containers.DeclarativeContainer):
    engine = providers.Dependency(instance_of=Engine)
    connection = providers.Resource(init_connection, engine=engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)

    # TODO: Where to put this?
    get_user_query = providers.Singleton(GetUserSQLQuery, connection=connection)
