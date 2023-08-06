import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.projects.entrypoints.endpoints import router


@pytest.fixture()
def app():
    app = FastAPI()
    app.include_router(router)

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)
