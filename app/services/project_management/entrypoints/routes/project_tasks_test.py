from datetime import date, datetime

import pytest

from app.services.project_management.entrypoints.dependencies import get_current_time
from app.services.project_management.test_utils.factories import build_project


@pytest.mark.integration
def test_tasks_endpoint_creates_task(session, client):
    # Given
    project = build_project(name="Test project")
    session.add(project)
    session.commit()

    # When
    response = client.post(
        f"/projects/{project.id}/tasks",
        json={"name": "Some task"},
    )

    # Then
    assert response.status_code == 303


@pytest.mark.integration
def test_task_complete_endpoint(session, client):
    # Given
    project = build_project(name="Test project")
    task = project.add_task(name="Test")
    session.add(project)
    session.commit()

    now = datetime(2012, 1, 18, 9, 30)
    client.app.dependency_overrides[get_current_time] = lambda: now

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/complete")

    # Then
    assert response.status_code == 303

    # TODO: Figure out how to fix this assertion
    # assert task.completed_at == now.date()


def test_task_complete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/complete")
    assert response.status_code == 404


@pytest.mark.integration
def test_task_incomplete_endpoint(session, client):
    # Given
    project = build_project(name="Test project")
    project.add_task(name="Test")

    task = project.add_task(name="Test")
    task.completed_at = date(2021, 1, 12)

    session.add(project)
    session.commit()

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/incomplete")

    # Then
    assert response.status_code == 303


def test_task_incomplete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/incomplete")
    assert response.status_code == 404
