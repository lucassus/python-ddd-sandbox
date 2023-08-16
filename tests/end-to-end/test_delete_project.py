from starlette import status
from starlette.testclient import TestClient


def test_delete_project(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == status.HTTP_200_OK
    project_id = response.json()["id"]

    response = client.put(f"/api/projects/{project_id}/archive")
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == status.HTTP_200_OK

    response = create_task(project_id=project_id, name="First task")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put(f"/api/projects/{project_id}/unarchive")
    assert response.status_code == status.HTTP_404_NOT_FOUND
