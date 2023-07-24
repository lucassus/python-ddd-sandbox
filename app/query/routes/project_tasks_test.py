from datetime import date

import pytest

from app.infrastructure.tables import projects_table, tasks_table


@pytest.mark.asyncio
async def test_tasks_endpoint(connection, client):
    # Given
    connection.execute(projects_table.insert().values([{"id": 1, "name": "Project One"}]))

    query = tasks_table.insert().values(
        [
            {
                "id": 1,
                "project_id": 1,
                "name": "Task One",
                "completed_at": None,
            },
            {
                "id": 2,
                "project_id": 1,
                "name": "Task Two",
                "completed_at": date(2021, 1, 6),
            },
            {
                "id": 3,
                "project_id": 1,
                "name": "Task Three",
                "completed_at": None,
            },
        ]
    )
    connection.execute(query)

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
async def test_task_endpoint_returns_task(connection, client):
    # Given
    connection.execute(
        projects_table.insert(),
        {"id": 1, "name": "Project One"},
    )

    connection.execute(
        tasks_table.insert(),
        {"id": 1, "project_id": 1, "name": "Task One"},
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
