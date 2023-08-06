from unittest.mock import Mock

import pytest

from app.query.dependencies import get_project
from app.query.queries.tasks import FindTaskQuery


@pytest.mark.asyncio()
async def test_task_endpoint_returns_404(app, client):
    # Given
    find_project_mock = Mock(return_value=Mock(id=1))
    app.dependency_overrides[get_project] = lambda: find_project_mock

    find_task_mock = Mock(return_value=None)
    app.dependency_overrides[FindTaskQuery] = lambda: find_task_mock

    # When
    response = await client.get("/projects/1/tasks/1")

    # Then
    assert response.status_code == 404
