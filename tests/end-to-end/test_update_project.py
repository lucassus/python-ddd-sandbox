from starlette import status
from starlette.testclient import TestClient

from app.modules.event_handlers import bus
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName


def test_update_project(current_user, client: TestClient):
    project_id = bus.execute(CreateProject(current_user.id, ProjectName("Project X")))

    response = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Project Y"},
        follow_redirects=True,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Project Y"
