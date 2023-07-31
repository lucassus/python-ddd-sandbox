from starlette.testclient import TestClient


def test_create_project(create_project, client: TestClient):
    response = create_project(name="Project X")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Project X"
