import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.entrypoints.routes import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)

    return TestClient(app)
