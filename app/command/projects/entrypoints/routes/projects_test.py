from unittest.mock import Mock

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.entities.project import ProjectID
from app.command.projects.entrypoints.dependencies import get_archivization_service, get_create_project
from app.command.shared_kernel.entities.user_id import UserID


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


def test_archive_project_endpoint(app: FastAPI, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)
    app.dependency_overrides[get_archivization_service] = lambda: archivization_service_mock

    # When
    response = client.put("/projects/123/archive")

    # Then
    assert response.status_code == 200
    archivization_service_mock.archive.assert_called_with(ProjectID(123))


def test_unarchive_project_endpoint(app: FastAPI, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)
    app.dependency_overrides[get_archivization_service] = lambda: archivization_service_mock

    # When
    response = client.put("/projects/124/unarchive")

    # Then
    assert response.status_code == 200
    archivization_service_mock.unarchive.assert_called_with(ProjectID(124))


def test_delete_project_endpoint(app: FastAPI, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)
    app.dependency_overrides[get_archivization_service] = lambda: archivization_service_mock

    # When
    response = client.delete("/projects/124")

    # Then
    assert response.status_code == 200
    archivization_service_mock.delete.assert_called_with(ProjectID(124))
