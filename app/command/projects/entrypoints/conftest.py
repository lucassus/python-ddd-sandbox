import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.projects.entrypoints import endpoints
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
    app.include_router(endpoints.router)

    return TestClient(app)
