import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.entrypoints import endpoints
from app.command.accounts.entrypoints.containers import Container


@pytest.fixture()
def container():
    container = Container()
    container.wire(modules=[endpoints])
    return container


@pytest.fixture()
def client(container):
    app = FastAPI()
    app.include_router(endpoints.router)

    return TestClient(app)
