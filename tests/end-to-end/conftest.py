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
def app():
    return create_app()


@pytest.fixture(scope="session")
def anonymous_client(app):
    return TestClient(app)


@pytest.fixture()
def register_user(anonymous_client: TestClient):
    def _register_user(email: str):
        return anonymous_client.post(
            "/api/users",
            json={"email": email, "password": "password"},
        )

    return _register_user


@pytest.fixture()
def client(register_user, app, anonymous_client):
    response = register_user("test@email.com")
    assert response.status_code == status.HTTP_200_OK  # noqa: S101

    response = anonymous_client.post(
        "/api/users/login",
        data={
            "grant_type": "password",
            "username": "test@email.com",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK  # noqa: S101
    token = response.json()["access_token"]

    return TestClient(
        app,
        headers={"Authorization": f"Bearer {token}"},
    )


@pytest.fixture()
def create_project(register_user, client: TestClient):
    def _create_project(name: str):
        return client.post(
            "/api/projects",
            json={"name": name},
        )

    return _create_project


@pytest.fixture()
def create_task(client: TestClient):
    def _create_task(project_id: int, name: str):
        return client.post(
            f"/api/projects/{project_id}/tasks",
            json={"name": name},
        )

    return _create_task
