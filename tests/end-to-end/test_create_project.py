from starlette import status
from starlette.testclient import TestClient

from app.modules.event_handlers import bus
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName


def test_create_project(client: TestClient):
    response = client.post(
        "/api/projects",
        json={"name": "Project X"},
    )

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


def test_list_projects(current_user, client: TestClient):
    # Given
    bus.execute(CreateProject(current_user.id, ProjectName("Project A")))
    bus.execute(CreateProject(current_user.id, ProjectName("Project B")))

    # When
    response = client.get("/api/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["projects"]) == 3


def test_list_projects_unauthenticated(anonymous_client):
    response = anonymous_client.get("/api/projects")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
