from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.modules.projects.application.tasks_service import TasksService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber
from app.modules.projects.entrypoints.containers import Container


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
    assert response.headers["Location"] == "/api/projects/123/tasks/1"
    mock_tasks_service.create_task.assert_called_once_with(project_id=ProjectID(123), name="Some task")


def test_task_endpoint_returns_404(container: Container, client: TestClient):
    # Given
    find_project_mock = Mock(return_value=Mock(id=1))
    # app.dependency_overrides[get_project] = lambda: find_project_mock

    find_task_mock = Mock(return_value=None)
    # app.dependency_overrides[FindTaskQuery] = lambda: find_task_mock

    # When
    response = client.get("/projects/1/tasks/1")

    # Then
    assert response.status_code == 404


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
    assert response.headers["Location"] == "/api/projects/665/tasks/667"
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
    assert response.headers["Location"] == "/api/projects/665/tasks/668"
    mock_tasks_service.incomplete_task.assert_called_once_with(ProjectID(665), TaskNumber(668))
