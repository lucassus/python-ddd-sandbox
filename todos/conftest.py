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
def engine() -> Engine:
    db_file = os.path.join(os.path.dirname(__file__), "../todos_test.db")
    engine = create_engine(
        f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
    )

    metadata.create_all(bind=engine)
    start_mappers()

    return engine


@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# TODO: Find a better idea
# TODO: Should tests be depended of sqla session?
@pytest.fixture
def uow(session):
    return UnitOfWork(session_factory=lambda: session)


@pytest.fixture
def client(uow):
    app = FastAPI()
    app.include_router(api_router)

    def _get_uow():
        with uow:
            yield uow

    app.dependency_overrides[get_uow] = _get_uow

    return TestClient(app)
