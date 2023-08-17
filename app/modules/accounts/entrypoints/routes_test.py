from unittest.mock import Mock

from starlette import status
from starlette.testclient import TestClient

from app.modules.accounts.application.queries.find_user_query import GetUserQuery
from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.entrypoints.containers import Container
from app.modules.shared_kernel.entities.user_id import UserID


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
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()


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


# TODO: Fix this test
def test_get_current_user_endpoint(container: Container, client: TestClient):
    # Given
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
    with container.get_user_query.override(get_user_mock):
        response = client.get("/users/me")

    # Then
    get_user_mock.assert_called_with(id=1)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }
