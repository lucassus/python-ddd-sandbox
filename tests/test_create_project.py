from starlette.testclient import TestClient


def test_create_project(register_user, client: TestClient):
    response = register_user(email="test@email.com")

    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.post(
        "/commands/projects",
        json={"user_id": user_id, "name": "Project X"},
    )

    assert response.status_code == 200
