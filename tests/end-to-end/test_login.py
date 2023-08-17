from starlette import status
from starlette.testclient import TestClient


def test_login(register_user, client: TestClient):
    response = register_user(email="just@email.com")
    assert response.status_code == status.HTTP_200_OK

    response = client.post(
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
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "just@email.com"
