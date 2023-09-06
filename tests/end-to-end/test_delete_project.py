from starlette import status
from starlette.testclient import TestClient

from app.modules.event_handlers import bus
from app.modules.projects.application.commands.archive_project import ArchiveProject
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName
from app.utc_datetime import utc_now


def test_delete_project(current_user, client: TestClient):
    # Given
    project_id = bus.execute(CreateProject(current_user.id, ProjectName("Project X")))
    bus.execute(ArchiveProject(project_id, now=utc_now()))

    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"name": "Test"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put(f"/api/projects/{project_id}/unarchive")
    assert response.status_code == status.HTTP_404_NOT_FOUND
