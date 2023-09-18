import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app.modules.accounts.entrypoints import routes
from app.modules.accounts.application.containers import AppContainer


@pytest.fixture(autouse=True)
def container():
    container = AppContainer(jwt_secret_key="test-secret")
    container.wire(
        [
            ".dependencies",
            ".routes",
        ],
    )

    return container


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(routes.router)

    return app


@pytest.fixture()
def client(app):
    return AsyncClient(app=app, base_url="http://test")
