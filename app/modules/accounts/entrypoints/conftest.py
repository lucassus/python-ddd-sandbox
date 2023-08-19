import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.accounts.containers import Container
from app.modules.accounts.entrypoints import routes

_container = Container(
    jwt_secret_key="test-secret",
)


@pytest.fixture(scope="session", autouse=True)
def _wire_container():
    _container.wire(
        modules=[
            ".dependencies",
            ".routes",
        ]
    )


@pytest.fixture()
def container():
    return _container


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(routes.router)

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
