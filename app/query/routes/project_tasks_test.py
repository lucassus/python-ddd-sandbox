from datetime import date

import pytest

from app.infrastructure.factories import create_project, create_task


@pytest.mark.asyncio
async def test_tasks_endpoint(connection, client):
    # Given
    project_id = create_project(connection, name="Project One").id

    create_task(connection, project_id, name="Task One")
    create_task(connection, project_id, name="Task Two", completed_at=date(2021, 1, 6))
    create_task(connection, project_id, name="Task Three")
    create_task(connection, name="Task Four")

    # When
    response = await client.get(f"/projects/{project_id}/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Task One", "completedAt": None},
        {"id": 2, "name": "Task Two", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Task Three", "completedAt": None},
    ]


@pytest.mark.asyncio
async def test_task_endpoint_returns_task(connection, client):
    # Given
    project_id = create_project(connection, name="Project One").id
    task_id = create_task(connection, project_id, name="Task One").id

    # When
    response = await client.get(f"/projects/{project_id}/tasks/{task_id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Task One", "completedAt": None}


@pytest.mark.asyncio
async def test_task_endpoint_returns_404(client):
    response = await client.get("/projects/1/tasks/1")
    assert response.status_code == 404
