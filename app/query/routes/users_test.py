from unittest.mock import Mock

import pytest

from app.infrastructure.factories import create_project, create_user
from app.query import schemas
from app.query.queries.users import FindUserQuery


@pytest.mark.asyncio
async def test_get_user(connection, client):
    # Given
    user_id = create_user(connection, email="test@email.com").id
    create_project(connection, user_id=user_id, name="Project One")
    create_project(connection, user_id=user_id, name="Project Two")

    # When
    response = await client.get(f"/users/{user_id}")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }


@pytest.mark.asyncio
async def test_get_user_with_mock(app, client):
    # Given
    find_user_mock = Mock(
        return_value=schemas.User(
            id=1,
            email="test@email.com",
            projects=[
                schemas.Project(id=1, name="Project One"),
                schemas.Project(id=2, name="Project Two"),
            ],
        )
    )
    app.dependency_overrides[FindUserQuery] = lambda: find_user_mock

    # When
    response = await client.get("/users/1")

    # Then
    find_user_mock.assert_called_with(id=1)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "test@email.com",
        "projects": [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ],
    }


@pytest.mark.asyncio
async def test_get_user_404(app, client):
    # Given
    find_user_mock = Mock(return_value=None)
    app.dependency_overrides[FindUserQuery] = lambda: find_user_mock

    # When
    response = await client.get("/users/2")

    # Then
    find_user_mock.assert_called_with(id=2)
    assert response.status_code == 404
