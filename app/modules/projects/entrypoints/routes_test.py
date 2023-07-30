from datetime import date, datetime

import pytest

from app.infrastructure.factories import create_project, create_task
from app.modules.projects.domain.entities import Task
from app.modules.projects.entrypoints.dependencies import get_current_time

# TODO: Use mock services in these tests


@pytest.mark.skip
def test_tasks_endpoint_creates_task(session, client):
    # Given
    project_id = create_project(session.connection(), name="Test project").id

    # When
    response = client.post(
        f"/projects/{project_id}/tasks",
        json={"name": "Some task"},
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303


@pytest.mark.skip
def test_task_complete_endpoint(session, client):
    # Given
    project_id = create_project(session.connection(), name="Test project").id
    task_number = create_task(session.connection(), project_id, name="Test task").number

    now = datetime(2012, 1, 18, 9, 30)
    client.app.dependency_overrides[get_current_time] = lambda: now

    # When
    response = client.put(
        f"/projects/{project_id}/tasks/{task_number}/complete",
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303

    task = session.get(Task, task_number)
    assert task.completed_at == now.date()


@pytest.mark.skip
def test_task_complete_endpoint_returns_404(client):
    response = client.put("/tasks/123/complete")
    assert response.status_code == 404


@pytest.mark.skip
def test_task_incomplete_endpoint(session, client):
    # Given
    project_id = create_project(session.connection(), name="Test project").id
    task_number = create_task(
        session.connection(),
        project_id,
        name="Test task",
        completed_at=date(2023, 1, 12),
    ).number

    # When
    response = client.put(
        f"/projects/{project_id}/tasks/{task_number}/incomplete",
        follow_redirects=False,
    )

    # Then
    assert response.status_code == 303


@pytest.mark.skip
def test_task_incomplete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/incomplete")
    assert response.status_code == 404
