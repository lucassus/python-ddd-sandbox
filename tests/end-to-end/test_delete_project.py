from starlette import status
from starlette.testclient import TestClient

from app.modules.event_handlers import bus
from app.modules.projects.application.commands.archive_project import ArchiveProject
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


def test_delete_project(client: TestClient):
    # Given
    # TODO: Find a better way to get current user_id
    user_id = UserID(client.get("/api/users/me").json()["id"])

    project_id = bus.execute(CreateProject(user_id=user_id, name=ProjectName("Project X")))
    bus.execute(ArchiveProject(project_id=project_id, now=utc_now()))

    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"name": "Test"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put(f"/api/projects/{project_id}/unarchive")
    assert response.status_code == status.HTTP_404_NOT_FOUND
