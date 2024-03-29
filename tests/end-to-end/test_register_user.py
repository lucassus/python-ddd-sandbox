from unittest.mock import ANY

from freezegun import freeze_time
from starlette import status
from starlette.testclient import TestClient

from app.modules.accounts.application.commands import RegisterUser
from app.modules.accounts.domain.password import Password
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.shared.message_bus import MessageBus


@freeze_time("2023-08-02 22:20:00")
def test_register_user(anonymous_client: TestClient):
    response = anonymous_client.post(
        "/api/users",
        json={"email": "test@email.com", "password": "password"},
    )
    assert response.status_code == status.HTTP_200_OK

    response = anonymous_client.post(
        "/api/users/login",
        data={
            "grant_type": "password",
            "username": "test@email.com",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    response = anonymous_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == {
        "id": ANY,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "My first project"},
        ],
    }

    project_id = data["projects"][0]["id"]
    response = anonymous_client.get(
        f"/api/projects/{project_id}/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "tasks": [
            {
                "number": 1,
                "name": "Sign up!",
                "completedAt": "2023-08-02T22:20:00",
            },
            {
                "number": 2,
                "name": "Watch the tutorial",
                "completedAt": None,
            },
            {
                "number": 3,
                "name": "Start using our awesome app",
                "completedAt": None,
            },
        ]
    }


def test_register_user_fail(bus: MessageBus, anonymous_client: TestClient):
    # Given
    bus.execute(RegisterUser(EmailAddress("taken@email.com"), Password("password")))

    # When
    response = anonymous_client.post(
        "/api/users",
        json={"email": "taken@email.com", "password": "password"},
    )

    # Then
    assert response.status_code == status.HTTP_409_CONFLICT
