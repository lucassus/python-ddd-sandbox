from unittest.mock import Mock

from app.command.projects.application.tasks_service import TasksService
from app.command.projects.entities.project import ProjectID
from app.command.projects.entities.task import TaskNumber
from app.command.projects.entrypoints.dependencies import get_tasks_service


def test_task_create_endpoint(client):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(1)
    client.app.dependency_overrides[get_tasks_service] = lambda: mock_tasks_service

    # When
    response = client.post(
        "/projects/123/tasks",
        json={"name": "Some task"},
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/123/tasks/1"
    mock_tasks_service.create_task.assert_called_once_with(project_id=ProjectID(123), name="Some task")


def test_task_complete_endpoint(client):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(667)
    client.app.dependency_overrides[get_tasks_service] = lambda: mock_tasks_service

    # When
    response = client.put(
        "/projects/665/tasks/667/complete",
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/665/tasks/667"
    mock_tasks_service.complete_task.assert_called_once_with(TaskNumber(667), project_id=ProjectID(665))


def test_task_incomplete_endpoint(client):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(668)
    client.app.dependency_overrides[get_tasks_service] = lambda: mock_tasks_service

    # When
    response = client.put(
        "/projects/665/tasks/668/incomplete",
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/665/tasks/668"
    mock_tasks_service.incomplete_task.assert_called_once_with(TaskNumber(668), project_id=ProjectID(665))
