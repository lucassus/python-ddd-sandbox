from starlette.testclient import TestClient


def test_delete_project(create_project, create_task, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = client.put(f"/commands/projects/{project_id}/archive")
    assert response.status_code == 200

    response = client.delete(f"/commands/projects/{project_id}")
    assert response.status_code == 200

    response = create_task(project_id=project_id, name="First task")
    assert response.status_code == 404

    response = client.put(f"/commands/projects/{project_id}/unarchive")
    assert response.status_code == 404
