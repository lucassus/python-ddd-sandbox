import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.query.routes import api_router


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(api_router)

    return app


@pytest.fixture()
def client(app):
    return AsyncClient(app=app, base_url="http://test")
