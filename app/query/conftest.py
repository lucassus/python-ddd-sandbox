import pytest
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.query.dependencies import get_database
from app.query.routes import api_router


@pytest.fixture
async def database(db_url):
    async with Database(db_url, force_rollback=True) as database:
        yield database


@pytest.fixture
def client(database):
    app = FastAPI()
    app.include_router(api_router)
    app.dependency_overrides[get_database] = lambda: database

    return AsyncClient(app=app, base_url="http://test")
