from unittest.mock import Mock

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.password import Password
from app.command.accounts.entrypoints.dependencies import get_register_user


def test_register_user_endpoint(app: FastAPI, client: TestClient):
    # Given
    register_user_mock = Mock(return_value=123)
    app.dependency_overrides[get_register_user] = lambda: register_user_mock

    # When
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
