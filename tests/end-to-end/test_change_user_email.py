from starlette import status
from starlette.testclient import TestClient


def test_change_user_email(client: TestClient):
    # Given
    response = client.get("/api/users/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "test@email.com"

    # When
    response = client.put(
        "/api/users/me",
        json={"email": "new@email.com"},
    )

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "new@email.com"
