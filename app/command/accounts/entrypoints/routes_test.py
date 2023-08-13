from unittest.mock import Mock

from starlette import status
from starlette.testclient import TestClient

from app.command.accounts.application.queries.find_user_query_protocol import FindUserQueryError, UserDetails
from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.errors import EmailAlreadyExistsException
from app.command.accounts.domain.password import Password
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


def test_get_user_endpoint(container: Container, client: TestClient):
    # Given
    find_user_mock = Mock(
        return_value=UserDetails(
            id=1,
            email="test@email.com",
            projects=[
                UserDetails.Project(id=1, name="Project One"),
                UserDetails.Project(id=2, name="Project Two"),
            ],
        )
    )

    # When
    with container.find_user_query.override(find_user_mock):
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


def test_get_user_endpoint_404(container: Container, client: TestClient):
    # Given
    find_user_mock = Mock(side_effect=FindUserQueryError(2))

    # When
    with container.find_user_query.override(find_user_mock):
        response = client.get("/users/2")

    # Then
    find_user_mock.assert_called_with(id=2)
    assert response.status_code == 404
