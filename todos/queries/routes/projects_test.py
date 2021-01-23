import pytest

from todos.infrastructure.database import database

# TODO: Figure out how to seed the database in a more convenient way
# TODO: See https://www.encode.io/databases/tests_and_migrations/


@pytest.mark.asyncio
async def test_projects_endpoint_returns_list_of_projects(client):
    # Given
    await database.execute("DELETE FROM projects")

    query = "INSERT INTO projects(name) VALUES (:name)"
    values = [
        {"name": "Project One"},
        {"name": "Project Two"},
    ]
    await database.execute_many(query=query, values=values)

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
    await database.execute("DELETE FROM projects")

    query = "INSERT INTO projects(name) VALUES (:name)"
    values = [{"name": "Project One"}]
    await database.execute_many(query=query, values=values)

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Project One"}


@pytest.mark.asyncio
async def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    # Given
    await database.execute("DELETE FROM projects")

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 404
