from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.entrypoints.containers import Container
from app.modules.projects.infrastructure.queries.project_queries import FindProjectQuery
from app.modules.shared_kernel.entities.user_id import UserID


def test_create_project_endpoint(container: Container, client: TestClient):
    # Given
    create_project_mock = Mock(return_value=1)

    # When
    with container.create_project.override(create_project_mock):
        response = client.post(
            "/projects",
            json={"user_id": 1, "name": "Test project"},
            follow_redirects=False,
        )

    # Then
    create_project_mock.assert_called_with(user_id=UserID(1), name="Test project")
    assert response.status_code == 303
    assert response.headers["location"] == "/api/projects/1"


def test_project_endpoint_responds_with_404_if_project_cannot_be_found(container: Container, client: TestClient):
    # Given
    find_project_mock = Mock(return_value=None)

    # When
    with container.find_project_query.override(find_project_mock):
        response = client.get("/projects/1")

    # Then
    assert response.status_code == 404


def test_list_projects_endpoint(container: Container, client: TestClient):
    # Given
    list_projects_query_mock = Mock(
        return_value=[
            {"id": 1, "name": "Test project"},
            {"id": 2, "name": "Test project 2"},
        ]
    )

    # When
    with container.list_projects_query.override(list_projects_query_mock):
        response = client.get("/projects")

    # Then
    assert response.status_code == 200


def test_update_project_endpoint(container: Container, client: TestClient):
    # Given
    update_project_mock = Mock()

    # When
    with container.update_project.override(update_project_mock):
        response = client.put(
            "/projects/123",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    update_project_mock.assert_called_with(ProjectID(123), "Test project")
    assert response.status_code == 303
    assert response.headers["location"] == "/api/projects/123"


def test_archive_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.put("/projects/123/archive")

    # Then
    assert response.status_code == 200
    archivization_service_mock.archive.assert_called_with(ProjectID(123))


def test_unarchive_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.put("/projects/124/unarchive")

    # Then
    assert response.status_code == 200
    archivization_service_mock.unarchive.assert_called_with(ProjectID(124))


def test_delete_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.delete("/projects/124")

    # Then
    assert response.status_code == 200
    archivization_service_mock.delete.assert_called_with(ProjectID(124))
