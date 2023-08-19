from typing import Iterator

from dependency_injector import containers, providers
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db import engine


def init_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        yield connection


class InfrastructureContainer(containers.DeclarativeContainer):
    engine = providers.Object(engine)
    connection = providers.Resource(init_connection, engine=engine)
    session_factory = providers.Singleton(sessionmaker, bind=engine)
