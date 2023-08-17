from starlette import status
from starlette.testclient import TestClient


def test_login(register_user, client: TestClient):
    response = register_user(email="just@email.com")
    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        "/api/users/login",
        json={
            "email": "just@email.com",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()

    token = response.json()["token"]
    response = client.get(
        "/api/users/me",
        headers={"x-authentication-token": token},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "just@email.com"
