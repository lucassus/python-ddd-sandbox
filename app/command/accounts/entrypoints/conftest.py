import pytest
from dependency_injector import providers
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.entrypoints import endpoints
from app.command.accounts.entrypoints.containers import Container


@pytest.fixture()
def container():
    container = Container(jwt_secret_key=providers.Object("secret-key"))  # TODO: Improve this
    container.wire()
    yield container
    container.unwire()


@pytest.fixture()
def client(container):
    app = FastAPI()
    app.include_router(endpoints.router)

    return TestClient(app)
