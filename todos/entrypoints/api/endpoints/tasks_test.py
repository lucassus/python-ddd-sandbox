from datetime import date

import pytest

from todos.domain.models import Task
from todos.entrypoints.api.dependencies import get_uow
from todos.interfaces.fake_unit_of_work import FakeUnitOfWork


def test_tasks_endpoint(client):
    # Given
    fake_uow = FakeUnitOfWork(
        tasks=[
            Task(name="Test task"),
            Task(name="The other task", completed_at=date(2021, 1, 6)),
            Task(name="Testing 123"),
        ]
    )
    client.app.dependency_overrides[get_uow] = lambda: fake_uow

    # When
    response = client.get("/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completed_at": None},
        {"id": 2, "name": "The other task", "completed_at": "2021-01-06"},
        {"id": 3, "name": "Testing 123", "completed_at": None},
    ]


@pytest.mark.integration
def test_tasks_endpoint_integration(session, client):
    # Given
    session.add(Task(name="Test task"))
    session.add(Task(name="The other task", completed_at=date(2021, 1, 6)))
    session.commit()

    # When
    response = client.get("/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test task", "completed_at": None},
        {"id": 2, "name": "The other task", "completed_at": "2021-01-06"},
    ]


@pytest.mark.integration
def test_tasks_endpoint_creates_task(client):
    response = client.post("/tasks", json={"name": "Some task"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Some task", "completed_at": None}


@pytest.mark.integration
def test_task_endpoint_returns_task(session, client):
    session.add(Task(name="Test name"))
    session.commit()

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test name", "completed_at": None}


def test_task_endpoint_returns_404(client):
    response = client.get("/tasks/1")
    assert response.status_code == 404


@pytest.mark.integration
def test_task_complete_endpoint(session, client):
    task = Task(name="Test")
    session.add(task)
    session.commit()

    response = client.put(f"/tasks/{task.id}/complete")

    assert response.status_code == 200
    # assert task.completed_at is not None


def test_task_complete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/complete")
    assert response.status_code == 404


@pytest.mark.integration
def test_task_incomplete_endpoint(session, client):
    task = Task(name="Test", completed_at=date(2021, 1, 12))
    session.add(task)
    session.commit()

    response = client.put(f"/tasks/{task.id}/incomplete")

    assert response.status_code == 200

    # TODO: Figure out how to write such tests
    # assert task.completed_at is None


def test_task_incomplete_endpoint_returns_404(client):
    response = client.put(f"/tasks/{123}/incomplete")
    assert response.status_code == 404
