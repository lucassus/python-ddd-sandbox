import pytest
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from todos.config import DATABASE_URL
from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables, drop_tables
from todos.queries.dependencies import get_database
from todos.queries.routes import api_router


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture
async def database():
    async with Database(DATABASE_URL, force_rollback=True) as database:
        yield database


@pytest.fixture
def client(database):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_database] = lambda: database

    return AsyncClient(app=app, base_url="http://test")
