from starlette import status
from starlette.testclient import TestClient


def test_change_user_email(register_user, client: TestClient):
    response = client.get("/api/users/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "test@email.com"

    response = client.put(
        "/api/users/me",
        json={"email": "new@email.com"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "new@email.com"


# TODO: Fix it...
# def test_change_user_email_unauthorized(client: TestClient):
#     response = client.put(
#         "/api/users/me",
#         json={"email": "test@email.com"},
#     )
#
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
