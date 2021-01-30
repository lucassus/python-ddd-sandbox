from datetime import date

import pytest

from app.infrastructure.tables import projects_table, tasks_table


@pytest.mark.asyncio
async def test_tasks_endpoint(database, client):
    # Given
    await database.execute(
        query=projects_table.insert(),
        values={"id": 1, "name": "Project One"},
    )

    await database.execute_many(
        query=tasks_table.insert(),
        values=[
            {"id": 1, "project_id": 1, "name": "Task One"},
            {
                "id": 2,
                "project_id": 1,
                "name": "Task Two",
                "completed_at": date(2021, 1, 6),
            },
            {"id": 3, "project_id": 1, "name": "Task Three"},
        ],
    )

    # When
    response = await client.get("/projects/1/tasks")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Task One", "completedAt": None},
        {"id": 2, "name": "Task Two", "completedAt": "2021-01-06"},
        {"id": 3, "name": "Task Three", "completedAt": None},
    ]


@pytest.mark.asyncio
async def test_task_endpoint_returns_task(database, client):
    # Given
    await database.execute(
        query=projects_table.insert(),
        values={"id": 1, "name": "Project One"},
    )

    await database.execute(
        query=tasks_table.insert(),
        values={"id": 1, "project_id": 1, "name": "Task One"},
    )

    # When
    response = await client.get("/projects/1/tasks/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Task One", "completedAt": None}


@pytest.mark.asyncio
async def test_task_endpoint_returns_404(client):
    response = await client.get("/projects/1/tasks/1")
    assert response.status_code == 404
