import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.projects.entrypoints import routes
from app.command.projects.entrypoints.containers import Container


@pytest.fixture()
def container():
    container = Container()
    container.wire()
    yield container
    container.unwire()


@pytest.fixture()
def client(container):
    app = FastAPI()
    app.include_router(routes.router)

    return TestClient(app)
