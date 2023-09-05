from starlette import status
from starlette.testclient import TestClient

from app.modules.event_handlers import bus
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName
from app.modules.shared_kernel.entities.user_id import UserID


def test_update_project(client: TestClient):
    # TODO: Find a better way to get current user_id
    user_id = UserID(client.get("/api/users/me").json()["id"])
    project_id = bus.execute(CreateProject(user_id=user_id, name=ProjectName("Project X")))

    response = client.put(
        f"/api/projects/{project_id}",
        json={"name": "Project Y"},
        follow_redirects=True,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Project Y"
