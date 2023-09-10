import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.accounts.entrypoints import routes
from app.modules.accounts.infrastructure.containers import Container


@pytest.fixture(autouse=True)
def container():
    container = Container(jwt_secret_key="test-secret")
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
    return TestClient(app)
