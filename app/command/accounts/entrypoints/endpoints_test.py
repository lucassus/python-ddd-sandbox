from unittest.mock import Mock

from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.errors import EmailAlreadyExistsException
from app.command.accounts.entities.password import Password


def test_register_user_endpoint(app: FastAPI, client: TestClient):
    # Given
    register_user_mock = Mock(return_value=123)

    # When
    with app.container.register_user.override(register_user_mock):
        response = client.post(
            "/users",
            json={"email": "test@email.com", "password": "password"},
            follow_redirects=False,
        )

    # Then
    register_user_mock.assert_called_with(
        email=EmailAddress("test@email.com"),
        password=Password("password"),
    )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/queries/users/123"


def test_register_user_endpoint_errors_handling(app: FastAPI, client: TestClient):
    # Given
    register_user_mock = Mock(side_effect=EmailAlreadyExistsException(EmailAddress("taken@email.com")))
    app.dependency_overrides[get_register_user] = lambda: register_user_mock

    # When
    response = client.post(
        "/users",
        json={"email": "taken@email.com", "password": "password"},
        follow_redirects=False,
    )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT
