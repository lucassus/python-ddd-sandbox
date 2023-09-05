from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.anys import AnyUUID
from app.modules.accounts.application.commands.register_user import RegisterUser
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.authentication_contract import AuthenticationContract
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus


def test_register_user_endpoint(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = client.post(
            "/users",
            json={
                "email": "test@email.com",
                "password": "password",
            },
            follow_redirects=False,
        )

    # Then
    bus_mock.execute.assert_called_with(
        RegisterUser(
            email=EmailAddress("test@email.com"),
            password=Password("password"),
        )
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("invalid", "password"),
        ("a@b.c", "password"),
        ("test@email.com", "short"),
        ("test@email.com", ""),
        ("", ""),
    ],
)
def test_register_user_endpoint_returns_422_when(client: TestClient, email, password):
    # When
    response = client.post(
        "/users",
        json={"email": email, "password": password},
    )

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_user_endpoint_errors_handling(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(MessageBus)
    bus_mock.execute.side_effect = EmailAlreadyExistsException(EmailAddress("taken@email.com"))

    # When
    with container.bus.override(bus_mock):
        response = client.post(
            "/users",
            json={"email": "taken@email.com", "password": "password"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_current_user_endpoint(
    container: Container,
    app: FastAPI,
    client: TestClient,
):
    # Given
    user_id = UserID.generate()

    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=user_id,
        email=EmailAddress("test@email.com"),
    )

    get_user_mock = Mock(
        return_value=GetUserQuery.Result(
            id=user_id,
            email="test@email.com",
            projects=[
                GetUserQuery.Result.Project(id=1, name="Project One"),
                GetUserQuery.Result.Project(id=2, name="Project Two"),
            ],
        )
    )

    # When
    with container.queries.get_user.override(get_user_mock):
        response = client.get("/users/me")

    # Then
    get_user_mock.assert_called_with(user_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(user_id),
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }
