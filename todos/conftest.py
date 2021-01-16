import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from todos.entrypoints.api import api_router
from todos.entrypoints.api.dependencies import get_uow
from todos.interfaces.db.tables import metadata, start_mappers
from todos.interfaces.db.unit_of_work import UnitOfWork
from todos.interfaces.fake_unit_of_work import FakeUnitOfWork

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
        raise AttributeError("Fixture session can be used only with integration tests!")

    session = Session(bind=db_connection)
    yield session
    session.close()


@pytest.fixture
def client(request):
    app = FastAPI()
    app.include_router(api_router)

    if "integration" in request.keywords:
        # For tests marked as "integration" create Unit Of Work
        # instance that uses the database...
        session = request.getfixturevalue("session")
        uow = UnitOfWork(session_factory=lambda: session)
    else:
        # ...otherwise go with the fake implementation.
        uow = FakeUnitOfWork(tasks=[])

    app.dependency_overrides[get_uow] = lambda: uow

    with uow:
        yield TestClient(app)
