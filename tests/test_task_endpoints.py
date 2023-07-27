from starlette.testclient import TestClient


def test_create_task(register_user, create_project, client: TestClient):
    response = register_user(email="test@email.com")
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = create_project(user_id=user_id, name="Project X")
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = client.post(
        f"/commands/projects/{project_id}/tasks",
        json={"name": "Testing..."},
        follow_redirects=True,
    )

    assert response.status_code == 200
    task_id = response.json()["id"]
    assert response.json()["name"] == "Testing..."
    assert response.json()["completedAt"] is None

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is not None

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_id}/incomplete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is None
