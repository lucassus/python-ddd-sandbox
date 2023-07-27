import httpx
import pytest
from starlette.testclient import TestClient

from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables
from app.main import create_app


@pytest.fixture(scope="function", autouse=True)
def prepare_db():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture(scope="session")
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def register_user(client: TestClient):
    def _register_user(email: str) -> httpx.Response:
        return client.post(
            "/commands/users",
            json={"email": email, "password": "password"},
            follow_redirects=True,
        )

    return _register_user


@pytest.fixture
def create_project(client: TestClient):
    def _create_project(user_id: int, name: str) -> httpx.Response:
        return client.post(
            "/commands/projects",
            json={"user_id": user_id, "name": name},
        )

    return _create_project
