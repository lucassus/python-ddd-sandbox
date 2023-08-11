from unittest.mock import Mock

from starlette.testclient import TestClient

from app.command.projects.application.tasks_service import TasksService
from app.command.projects.domain.project import ProjectID
from app.command.projects.domain.task import TaskNumber
from app.command.projects.entrypoints.containers import Container


def test_task_create_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(1)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.post(
            "/projects/123/tasks",
            json={"name": "Some task"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/123/tasks/1"
    mock_tasks_service.create_task.assert_called_once_with(project_id=ProjectID(123), name="Some task")


def test_task_complete_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(667)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.put(
            "/projects/665/tasks/667/complete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/665/tasks/667"
    mock_tasks_service.complete_task.assert_called_once_with(ProjectID(665), TaskNumber(667))


def test_task_incomplete_endpoint(container: Container, client: TestClient):
    # Given
    mock_tasks_service = Mock(spec=TasksService)
    mock_tasks_service.create_task.return_value = TaskNumber(668)

    # When
    with container.tasks_service.override(mock_tasks_service):
        response = client.put(
            "/projects/665/tasks/668/incomplete",
            follow_redirects=False,
        )

    # Then
    assert response.status_code == 303
    assert response.headers["Location"] == "/queries/projects/665/tasks/668"
    mock_tasks_service.incomplete_task.assert_called_once_with(ProjectID(665), TaskNumber(668))
