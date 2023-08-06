import httpx
import pytest
from starlette import status
from starlette.testclient import TestClient

from app import create_app
from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables


@pytest.fixture(autouse=True)
def _prepare_db():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture(scope="session")
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def register_user(client: TestClient):
    def _register_user(email: str) -> httpx.Response:
        return client.post(
            "/commands/users",
            json={"email": email, "password": "password"},
            follow_redirects=True,
        )

    return _register_user


@pytest.fixture()
def create_project(register_user, client: TestClient):
    def _create_project(name: str, user_id: int | None = None) -> httpx.Response:
        if user_id is None:
            response = register_user("test@email.com")
            assert response.status_code == status.HTTP_200_OK  # noqa: S101
            user_id = response.json()["id"]

        return client.post(
            "/commands/projects",
            json={"user_id": user_id, "name": name},
        )

    return _create_project


@pytest.fixture()
def create_task(client: TestClient):
    def _create_task(project_id: int, name: str) -> httpx.Response:
        return client.post(
            f"/commands/projects/{project_id}/tasks",
            json={"name": name},
        )

    return _create_task
