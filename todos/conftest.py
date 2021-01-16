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
from todos.service_layer.unit_of_work import UnitOfWork


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    db_file = os.path.join(os.path.dirname(__file__), "../todos_test.db")
    engine = create_engine(
        f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
    )

    metadata.create_all(bind=engine)
    start_mappers()

    return engine


@pytest.fixture
def db_connection(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(db_connection):
    session = Session(bind=db_connection)
    yield session
    session.close()


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(api_router)

    def _get_uow():
        with UnitOfWork(session_factory=lambda: session) as uow:
            yield uow

    app.dependency_overrides[get_uow] = _get_uow

    return TestClient(app)
