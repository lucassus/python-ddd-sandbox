from starlette import status
from starlette.testclient import TestClient

from app.anys import AnyUUID
from app.modules.event_handlers import bus
from app.modules.projects.application.commands.create_project import CreateProject
from app.modules.projects.domain.project import ProjectName
from app.modules.shared_kernel.entities.user_id import UserID


def test_create_task(client: TestClient, create_task):
    # TODO: Find a better way to get current user_id
    user_id = UserID(client.get("/api/users/me").json()["id"])
    project_id = bus.execute(CreateProject(user_id=user_id, name=ProjectName("Project X")))

    response = create_task(project_id=project_id, name="First task")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "number": 1,
        "name": "First task",
        "createdBy": AnyUUID,
        "completedAt": None,
    }

    response = create_task(project_id=project_id, name="Second task")
    assert response.status_code == status.HTTP_200_OK


def test_complete_task(client: TestClient, create_task):
    # TODO: Find a better way to get current user_id
    user_id = UserID(client.get("/api/users/me").json()["id"])
    project_id = bus.execute(CreateProject(user_id=user_id, name=ProjectName("Project X")))

    response = create_task(project_id=project_id, name="First task")
    task_number = response.json()["number"]

    response = client.put(f"/api/projects/{project_id}/tasks/{task_number}/complete")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is not None

    response = client.put(f"/api/projects/{project_id}/tasks/{task_number}/incomplete")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completedAt"] is None
