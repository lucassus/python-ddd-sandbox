from starlette.testclient import TestClient


def test_register_user(register_user, client: TestClient):
    response = register_user(email="test@email.com")

    assert response.status_code == 200
    user_id = response.json()["id"]
    assert response.json() == {
        "id": user_id,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "My first project"},
        ],
    }

    project_id = response.json()["projects"][0]["id"]
    response = client.get(f"/queries/projects/{project_id}/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Sign up!", "completedAt": "2023-07-27"},
        {"id": 2, "name": "Watch the tutorial", "completedAt": None},
        {"id": 3, "name": "Start using our awesome app", "completedAt": None},
    ]

    response = client.put(
        f"/commands/users/{user_id}",
        json={"email": "new@email.com"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@email.com"
