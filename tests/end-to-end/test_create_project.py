from starlette import status
from starlette.testclient import TestClient


def test_create_project(create_project, client: TestClient):
    response = create_project(name="Project X")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Project X"
