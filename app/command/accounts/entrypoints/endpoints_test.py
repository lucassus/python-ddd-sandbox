from unittest.mock import Mock

from starlette import status
from starlette.testclient import TestClient

from app.command.accounts.application.authenticate import AuthenticationError
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.errors import EmailAlreadyExistsException
from app.command.accounts.entities.password import Password
from app.command.accounts.entrypoints.containers import Container


def test_register_user_endpoint(container: Container, client: TestClient):
    # Given
    register_user_mock = Mock(return_value=123)

    # When
    with container.register_user.override(register_user_mock):
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


def test_login_endpoint(container: Container, client: TestClient):
    # Given
    authenticate_mock = Mock(return_value="some-token")

    # When
    with container.authenticate.override(authenticate_mock):
        response = client.post(
            "/users/login",
            json={"email": "test@email.com", "password": "password"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_200_OK
    authenticate_mock.assert_called_with(
        email=EmailAddress("test@email.com"),
        password=Password("password"),
    )
    assert response.json()["token"] == "some-token"


def test_login_endpoint_with_invalid_credentials(container: Container, client: TestClient):
    # Given
    authenticate_mock = Mock(side_effect=AuthenticationError())

    # When
    with container.authenticate.override(authenticate_mock):
        response = client.post(
            "/users/login",
            json={"email": "invalid@email.com", "password": "invalid-password"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_user_endpoint_errors_handling(container: Container, client: TestClient):
    # Given
    register_user_mock = Mock(side_effect=EmailAlreadyExistsException(EmailAddress("taken@email.com")))

    # When
    with container.register_user.override(register_user_mock):
        response = client.post(
            "/users",
            json={"email": "taken@email.com", "password": "password"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT
