import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.infrastructure.tables import create_tables
from app.services.projects.adapters.mappers import start_mappers

start_mappers()


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    database_path = os.path.join(os.path.dirname(__file__), "../../../test.db")
    engine = create_engine(
        f"sqlite:///{database_path}", connect_args={"check_same_thread": False}
    )

    create_tables(engine)

    return engine


@pytest.fixture
def db_connection(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(request, db_connection):
    if "integration" not in request.keywords:
        raise AttributeError(
            "Fixture session can be used only with tests marked as integration!"
        )

    session = Session(bind=db_connection)
    yield session
    session.close()
