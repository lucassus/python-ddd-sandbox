from starlette import status
from starlette.testclient import TestClient


def test_change_user_email(register_user, client: TestClient):
    response = register_user(email="just@email.com")
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["token"]

    response = client.put(
        "/api/users/me",
        json={"email": "new@email.com"},
        headers={"x-authentication-token": token},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "new@email.com"
