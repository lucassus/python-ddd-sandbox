import pytest

from todos.infrastructure.database import database

# TODO: Figure out how to seed the database in a more convenient way
# TODO: See https://www.encode.io/databases/tests_and_migrations/
from todos.infrastructure.tables import projects_table

# TODO: See and example how to setup the db:
#  https://github.com/encode/databases/blob/master/tests/test_integration.py


@pytest.mark.asyncio
async def test_projects_endpoint_returns_list_of_projects(client):
    # Given
    # await database.execute(projects_table.delete())

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
async def test_project_endpoint_returns_the_project(client):
    # Given
    # await database.execute(projects_table.delete())

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
    # Given
    # await database.execute(projects_table.delete())

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 404
