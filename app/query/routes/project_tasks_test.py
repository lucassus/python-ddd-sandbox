from datetime import date

import pytest

from app.infrastructure.factories import create_project, create_task


@pytest.mark.asyncio
async def test_tasks_endpoint(connection, client):
    # Given
    project = create_project(connection, name="Project One")

    create_task(connection, number=1, project=project, name="Task One")
    create_task(connection, number=2, project=project, name="Task Two", completed_at=date(2021, 1, 6))
    create_task(connection, number=3, project=project, name="Task Three")
    create_task(connection, number=1, name="Task Four")

    # When
    response = await client.get(f"/projects/{project.id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"number": 1, "name": "Task One", "completedAt": None},
        {"number": 2, "name": "Task Two", "completedAt": "2021-01-06"},
        {"number": 3, "name": "Task Three", "completedAt": None},
    ]


@pytest.mark.asyncio
async def test_task_endpoint_returns_task(connection, client):
    # Given
    project = create_project(connection, name="Project One")
    task = create_task(connection, project=project, number=1, name="Task One")

    # When
    response = await client.get(f"/projects/{project.id}/tasks/{task.number}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"number": 1, "name": "Task One", "completedAt": None}


@pytest.mark.asyncio
async def test_task_endpoint_returns_404(client):
    response = await client.get("/projects/1/tasks/1")
    assert response.status_code == 404
