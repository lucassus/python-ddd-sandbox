from starlette import status
from starlette.testclient import TestClient


def test_create_project(create_project):
    response = create_project(name="Project X")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Project X"


def test_create_project_unauthenticated(anonymous_client):
    response = anonymous_client.post(
        "/api/projects",
        json={"name": "Project Y"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_projects(create_project, client: TestClient):
    # Given
    response = create_project(name="Project A")
    assert response.status_code == status.HTTP_200_OK

    response = create_project(name="Project B")
    assert response.status_code == status.HTTP_200_OK

    # When
    response = client.get("/api/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["projects"]) == 3


def test_list_projects_unauthenticated(anonymous_client):
    response = anonymous_client.get("/api/projects")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
