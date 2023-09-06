import pytest
from starlette import status
from starlette.testclient import TestClient

from app import create_app
from app.infrastructure.db import engine
from app.infrastructure.tables import create_tables, drop_tables
from app.modules.accounts.application.commands.register_user import RegisterUser
from app.modules.accounts.domain.password import Password
from app.modules.event_handlers import bus
from app.modules.shared_kernel.entities.email_address import EmailAddress


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
def client(app, anonymous_client):
    bus.execute(
        RegisterUser(
            email=EmailAddress("test@email.com"),
            password=Password("password"),
        ),
    )

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
