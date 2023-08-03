from unittest.mock import Mock

import pytest

from app.query.queries.projects import FindProjectQuery


@pytest.mark.asyncio
async def test_project_endpoint_responds_with_404_if_project_cannot_be_found(app, client):
    # Given
    find_project_mock = Mock(return_value=None)
    app.dependency_overrides[FindProjectQuery] = lambda: find_project_mock

    # When
    response = await client.get("/projects/1")

    # Then
    assert response.status_code == 404
