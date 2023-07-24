import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.query.queries.abstract_query import get_connection
from app.query.routes import api_router


@pytest.fixture
def connection(db_engine, prepare_db):
    with db_engine.begin() as connection:
        yield connection


@pytest.fixture
def client(connection):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_connection] = lambda: connection

    return AsyncClient(app=app, base_url="http://test")
