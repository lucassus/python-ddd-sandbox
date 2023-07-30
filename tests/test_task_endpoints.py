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
        json={"name": "First task"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    response = client.post(
        f"/commands/projects/{project_id}/tasks",
        json={"name": "Second task"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    task_number = response.json()["number"]
    assert response.json()["name"] == "Second task"
    assert response.json()["completedAt"] is None

    # TODO: Move it to the separate scenario
    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/complete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is not None

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/incomplete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is None
