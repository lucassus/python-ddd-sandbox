import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from todos.entrypoints.api import api_router
from todos.entrypoints.api.dependencies import get_session
from todos.interfaces.db.tables import metadata, start_mappers


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


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_session] = lambda: session

    return TestClient(app)
