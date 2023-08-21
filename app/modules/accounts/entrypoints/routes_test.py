from unittest.mock import Mock

from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints.containers import Container
from app.modules.accounts.entrypoints.dependencies import get_current_user
from app.modules.accounts.queries.find_user_query import GetUserQuery
from app.modules.authentication_contract import AuthenticationContract
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


def test_register_user_endpoint(container: Container, client: TestClient):
    # Given
    register_user_mock = Mock(return_value=123)

    # When
    with container.application.register_user.override(register_user_mock):
        response = client.post(
            "/users",
            json={
                "email": "test@email.com",
                "password": "password",
            },
            follow_redirects=False,
        )

    # Then
    register_user_mock.assert_called_with(
        email=EmailAddress("test@email.com"),
        password=Password("password"),
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_register_user_endpoint_errors_handling(container: Container, client: TestClient):
    # Given
    register_user_mock = Mock(side_effect=EmailAlreadyExistsException(EmailAddress("taken@email.com")))

    # When
    with container.application.register_user.override(register_user_mock):
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
    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=UserID(1),
        email=EmailAddress("test@email.com"),
    )

    get_user_mock = Mock(
        return_value=GetUserQuery.Result(
            id=1,
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
    get_user_mock.assert_called_with(1)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }
