from starlette.testclient import TestClient


def test_create_task(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = create_task(project_id=project_id, name="First task")
    assert response.status_code == 200

    response = create_task(project_id=project_id, name="Second task")
    assert response.status_code == 200


def test_complete_task(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = create_task(project_id=project_id, name="First task")
    task_number = response.json()["number"]

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/complete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is not None

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/incomplete")
    assert response.status_code == 200
    assert response.json()["completedAt"] is None
