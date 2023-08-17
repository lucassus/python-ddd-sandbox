import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.modules.accounts.entrypoints import routes
from app.modules.accounts.entrypoints.containers import Container

_container = Container(
    jwt_secret_key="test-secret",
)


@pytest.fixture(scope="session", autouse=True)
def _wire_container():
    _container.wire()


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
