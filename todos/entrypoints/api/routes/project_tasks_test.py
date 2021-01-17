from datetime import date, datetime

import pytest

from todos.entrypoints.api.dependencies import get_current_time, get_uow
from todos.test_utils.factories import build_project, build_task
from todos.test_utils.fake_unit_of_work import FakeUnitOfWork


def test_tasks_endpoint(client):
    # Given
    project = build_project(id=1)
    project.tasks.extend(
        [
            build_task(id=1, name="Test task"),
            build_task(id=2, name="The other task", completed_at=date(2021, 1, 6)),
            build_task(id=3, name="Testing 123"),
        ]
    )

    fake_uow = FakeUnitOfWork(
        projects=[
            project,
            build_project(id=2, name="Other Project"),
        ]
    )
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get("/projects/1/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completedAt": None},
        {"id": 2, "name": "The other task", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Testing 123", "completedAt": None},
    ]


@pytest.mark.integration
def test_tasks_endpoint_integration(session, client):
    # Given
    project = build_project()
    project.tasks = [
        build_task(name="Test task"),
        build_task(name="The other task", completed_at=date(2021, 1, 6)),
    ]
    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completedAt": None},
        {"id": 2, "name": "The other task", "completedAt": "2021-01-06"},
    ]


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
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Some task", "completedAt": None}


@pytest.mark.integration
def test_task_endpoint_returns_task(session, client):
    # Given
    project = build_project()
    task = build_task(name="Test name")
    project.tasks = [task]
    session.add(project)
    session.commit()

    # When
    response = client.get(f"/projects/{project.id}/tasks/{task.id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completedAt": None}


def test_task_endpoint_returns_404(client):
    response = client.get("/tasks/1")
    assert response.status_code == 404


@pytest.mark.integration
def test_task_complete_endpoint(session, client):
    # Given
    project = build_project(name="Test project")
    project.tasks = [build_task(name="Test")]
    session.add(project)
    session.commit()

    now = datetime(2012, 1, 18, 9, 30)
    client.app.dependency_overrides[get_current_time] = lambda: now

    task = project.tasks[0]

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/complete")

    # Then
    assert response.status_code == 200
    assert task.completed_at == now.date()


def test_task_complete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/complete")
    assert response.status_code == 404


@pytest.mark.integration
def test_task_incomplete_endpoint(session, client):
    # Given
    project = build_project(name="Test project")
    project.tasks = [build_task(name="Test", completed_at=date(2021, 1, 12))]
    session.add(project)
    session.commit()

    task = project.tasks[0]

    # When
    response = client.put(f"/projects/{project.id}/tasks/{task.id}/incomplete")

    # Then
    assert response.status_code == 200
    assert task.completed_at is None


def test_task_incomplete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/incomplete")
    assert response.status_code == 404
