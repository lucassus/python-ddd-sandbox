from unittest.mock import ANY, Mock

from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.anys import AnyUUID
from app.modules.projects.application.commands import (
    ArchiveProject,
    CreateProject,
    DeleteProject,
    UnarchiveProject,
    UpdateProject,
)
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.infrastructure.containers import Container
from app.shared.message_bus import MessageBus


def test_create_project_endpoint(container: Container, app: FastAPI, client: TestClient):
    # Given
    bus_mock = Mock(spec=MessageBus)
    bus_mock.execute.return_value = ProjectID(1)

    # When
    with container.bus.override(bus_mock):
        response = client.post(
            "/projects",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/1"
    bus_mock.execute.assert_called_with(
        CreateProject(
            user_id=AnyUUID,  # type: ignore
            name=ProjectName("Test project"),
        )
    )


def test_list_projects_endpoint(container: Container, client: TestClient):
    # Given
    list_projects_query_mock = Mock(
        return_value={
            "projects": [
                {"id": 1, "name": "Test project"},
                {"id": 2, "name": "Test project 2"},
            ]
        }
    )

    # When
    with container.queries.list_projects.override(list_projects_query_mock):
        response = client.get("/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK


def test_update_project_endpoint(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = client.put(
            "/projects/123",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/123"
    bus_mock.execute.assert_called_with(
        UpdateProject(
            project_id=ProjectID(123),
            name=ProjectName("Test project"),
        )
    )


def test_archive_project_endpoint(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = client.put("/projects/123/archive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(
        ArchiveProject(
            project_id=ProjectID(123),
            now=ANY,
        )
    )


def test_unarchive_project_endpoint(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = client.put("/projects/124/unarchive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(UnarchiveProject(project_id=ProjectID(124)))


def test_delete_project_endpoint(container: Container, client: TestClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = client.delete("/projects/124")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(DeleteProject(project_id=ProjectID(124), now=ANY))
