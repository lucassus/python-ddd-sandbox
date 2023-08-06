from unittest.mock import Mock

from starlette.testclient import TestClient

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.entities.project import ProjectID
from app.command.projects.entrypoints.containers import Container
from app.command.shared_kernel.entities.user_id import UserID


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
    assert response.headers["location"] == "/queries/projects/1"


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
    assert response.headers["location"] == "/queries/projects/123"


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
