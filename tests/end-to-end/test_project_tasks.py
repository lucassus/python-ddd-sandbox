from starlette import status
from starlette.testclient import TestClient

from app.modules import bus
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.application.commands.create_task import CreateTask
from app.modules.projects.domain.project import ProjectName


def test_create_task(current_user, client: TestClient):
    # Given
    project_id = bus.execute(CreateProject(current_user.id, ProjectName("Project X")))

    # When
    response = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"name": "First task"},
    )

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "number": 1,
        "name": "First task",
        "completedAt": None,
    }


def test_complete_task(current_user, client: TestClient):
    # Given
    project_id = bus.execute(CreateProject(current_user.id, ProjectName("Project X")))
    task_number = bus.execute(CreateTask(project_id, name="First task"))

    # When
    response = client.put(f"/api/projects/{project_id}/tasks/{task_number}/complete")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is not None

    # When
    response = client.put(f"/api/projects/{project_id}/tasks/{task_number}/incomplete")

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is None
