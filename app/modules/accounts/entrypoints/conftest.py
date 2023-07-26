import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.modules.accounts.entrypoints.routes import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)

    return app


@pytest.fixture
def client(app):
    return TestClient(app)
