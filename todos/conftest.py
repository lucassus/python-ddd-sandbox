import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from todos.adapters.db.tables import metadata, start_mappers

start_mappers()


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    db_file = os.path.join(os.path.dirname(__file__), "../todos_test.db")
    engine = create_engine(
        f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
    )

    metadata.create_all(bind=engine)

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
