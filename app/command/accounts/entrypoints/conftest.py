import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.entrypoints import endpoints
from app.command.accounts.entrypoints.containers import Container


@pytest.fixture
def app():
    container = Container()
    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app


@pytest.fixture
def client(app):
    return TestClient(app)
