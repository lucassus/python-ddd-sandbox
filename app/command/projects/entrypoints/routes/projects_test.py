from unittest.mock import Mock

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.projects.entrypoints.dependencies import get_create_project
from app.command.shared_kernel.user_id import UserID


def test_create_project_endpoint(app: FastAPI, client: TestClient):
    # Given
    create_project_mock = Mock(return_value=1)
    app.dependency_overrides[get_create_project] = lambda: create_project_mock

    # When
    response = client.post(
        "/projects",
        json={"user_id": 1, "name": "Test project"},
        follow_redirects=False,
    )

    # Then
    create_project_mock.assert_called_with(user_id=UserID(1), name="Test project")
    assert response.status_code == 303
    assert response.headers["location"] == "/queries/projects/1"
