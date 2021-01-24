import pytest

from todos.infrastructure.tables import projects_table

# TODO: Figure out how to seed the database in a more convenient way


@pytest.mark.asyncio
async def test_projects_endpoint_returns_list_of_projects(database, client):
    # Given
    await database.execute_many(
        query=projects_table.insert(),
        values=[
            {"name": "Project One"},
            {"name": "Project Two"},
        ],
    )

    # When
    response = await client.get("/projects")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Project One"},
        {"id": 2, "name": "Project Two"},
    ]


@pytest.mark.asyncio
async def test_project_endpoint_returns_the_project(database, client):
    # Given
    await database.execute(
        query=projects_table.insert(),
        values={"name": "Project One"},
    )

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Project One"}


@pytest.mark.asyncio
async def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    response = await client.get("/projects/1")
    assert response.status_code == 404
