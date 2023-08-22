from starlette import status
from starlette.testclient import TestClient


def test_login(register_user, anonymous_client: TestClient):
    response = register_user(email="just@email.com")
    assert response.status_code == status.HTTP_200_OK

    response = anonymous_client.post(
        "/api/users/login",
        data={
            "grant_type": "password",
            "username": "just@email.com",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

    token = response.json()["access_token"]
    response = anonymous_client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "just@email.com"


def test_login_with_invalid_credentials(anonymous_client: TestClient):
    response = anonymous_client.post(
        "/api/users/login",
        data={
            "grant_type": "password",
            "username": "invalid@email.com",
            "password": "invalid-passwd",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"
