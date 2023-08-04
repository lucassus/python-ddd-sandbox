from starlette.testclient import TestClient


def test_change_user_email(register_user, client: TestClient):
    response = register_user(email="just@email.com")
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.put(
        f"/commands/users/{user_id}",
        json={"email": "new@email.com"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@email.com"
