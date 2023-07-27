from starlette.testclient import TestClient


def test_create_project(client: TestClient):
    # TODO: Create a helper function to register a user
    response = client.post(
        "/commands/users",
        json={"email": "test@email.com", "password": "password"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.post(
        "/commands/projects",
        json={"user_id": user_id, "name": "Project X"},
    )

    assert response.status_code == 200
