import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import StaticPool

from todos.api import api_router
from todos.api.dependencies import get_session
from todos.db.tables import metadata, start_mappers


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # A pool for exactly one connection
    )

    metadata.create_all(bind=engine)
    start_mappers()

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    yield session
    clear_mappers()


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_session] = lambda: session

    return TestClient(app)
