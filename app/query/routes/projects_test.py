import pytest

from app.infrastructure.factories import create_project


@pytest.mark.asyncio
async def test_projects_endpoint_returns_list_of_projects(connection, client):
    # Given
    create_project(connection, name="Project One")
    create_project(connection, name="Project Two")

    # When
    response = await client.get("/projects")

    # Then
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Project One"},
        {"id": 2, "name": "Project Two"},
    ]


@pytest.mark.asyncio
async def test_project_endpoint_returns_the_project(connection, client):
    # Given
    user_id = create_project(connection, name="Project One").id
    project_id = create_project(connection, user_id=user_id, name="Project One").id

    # When
    response = await client.get(f"/projects/{project_id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": project_id,
        "name": "Project One",
    }


@pytest.mark.asyncio
async def test_project_endpoint_responds_with_404_if_project_cannot_be_found(client):
    response = await client.get("/projects/1")
    assert response.status_code == 404
