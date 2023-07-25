import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.query.queries.abstract_query import get_connection
from app.query.routes import api_router


@pytest.fixture
def app(connection):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_connection] = lambda: connection

    return app


@pytest.fixture
def client(app):
    return AsyncClient(app=app, base_url="http://test")
