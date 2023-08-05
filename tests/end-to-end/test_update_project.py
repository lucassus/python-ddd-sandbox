from starlette.testclient import TestClient


def test_update_project(create_project, client: TestClient):
    response = create_project(name="Project X")
    assert response.status_code == 200
    project_id = response.json()["id"]

    response = client.put(
        f"/commands/projects/{project_id}",
        json={"name": "Project Y"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Project Y"