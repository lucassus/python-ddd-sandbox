from unittest.mock import Mock

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.entities.email_address import EmailAddress
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
    assert response.status_code == 303
    assert response.headers["location"] == "/queries/users/123"
