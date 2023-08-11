from unittest.mock import Mock

import pytest
from starlette import status
from starlette.testclient import TestClient

from app.command.accounts.application.queries import schemas
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.errors import EmailAlreadyExistsException
from app.command.accounts.entities.password import Password
from app.command.accounts.entrypoints.containers import Container
from app.command.accounts.infrastructure.queries.find_user_query import FindUserQuery


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
    assert response.headers["location"] == "/commands/users/123"


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


def test_get_user(client):
    # Given
    find_user_mock = Mock(
        return_value=schemas.UserDetails(
            id=1,
            email="test@email.com",
            projects=[
                schemas.Project(id=1, name="Project One"),
                schemas.Project(id=2, name="Project Two"),
            ],
        )
    )
    client.app.dependency_overrides[FindUserQuery] = lambda: find_user_mock

    # When
    response = client.get("/users/1")

    # Then
    find_user_mock.assert_called_with(id=1)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }


def test_get_user_404(client):
    # Given
    find_user_mock = Mock(return_value=None)
    client.app.dependency_overrides[FindUserQuery] = lambda: find_user_mock

    # When
    response = client.get("/users/2")

    # Then
    find_user_mock.assert_called_with(id=2)
    assert response.status_code == 404
