import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.modules.projects.entrypoints import routes
from app.modules.projects.entrypoints.containers import Container

_container = Container()


@pytest.fixture(scope="session", autouse=True)
def _wire_container():
    _container.wire()


@pytest.fixture()
def container():
    return _container


@pytest.fixture()
def client():
    app = FastAPI()
    app.include_router(routes.router)

    return TestClient(app)