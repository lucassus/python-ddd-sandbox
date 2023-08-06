from starlette import status
from starlette.testclient import TestClient


def test_create_task(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == status.HTTP_200_OK
    project_id = response.json()["id"]

    response = create_task(project_id=project_id, name="First task")
    assert response.status_code == status.HTTP_200_OK

    response = create_task(project_id=project_id, name="Second task")
    assert response.status_code == status.HTTP_200_OK


def test_complete_task(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == status.HTTP_200_OK
    project_id = response.json()["id"]

    response = create_task(project_id=project_id, name="First task")
    task_number = response.json()["number"]

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/complete")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is not None

    response = client.put(f"/commands/projects/{project_id}/tasks/{task_number}/incomplete")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is None
