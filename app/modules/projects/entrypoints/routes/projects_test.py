from unittest.mock import Mock

from fastapi import FastAPI
from starlette import status
from starlette.testclient import TestClient

from app.modules.projects.application.archivization_service import ArchivizationService
from app.modules.projects.application.queries.project_queries import GetProjectQuery
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.entrypoints.containers import Container
from app.modules.shared_kernel.entities.user_id import UserID
from modules.authentication_contract import AuthenticationContract
from modules.projects.entrypoints.dependencies import get_current_user
from modules.shared_kernel.entities.email_address import EmailAddress


def test_create_project_endpoint(container: Container, app: FastAPI, client: TestClient):
    # Given
    app.dependency_overrides[get_current_user] = lambda: AuthenticationContract.CurrentUserDTO(
        id=UserID(1),
        email=EmailAddress("test@email.com"),
    )

    create_project_mock = Mock(return_value=1)

    # When
    with container.create_project.override(create_project_mock):
        response = client.post(
            "/projects",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    create_project_mock.assert_called_with(user_id=UserID(1), name="Test project")
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/1"


def test_get_project_endpoint_responds_with_404_if_project_cannot_be_found(container: Container, client: TestClient):
    # Given
    get_project_query_mock = Mock(side_effect=GetProjectQuery.NotFoundError(id=ProjectID(1)))

    # When
    with container.get_project_query.override(get_project_query_mock):
        response = client.get("/projects/1")

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND


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
    with container.list_projects_query.override(list_projects_query_mock):
        response = client.get("/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK


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
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/123"


def test_archive_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.put("/projects/123/archive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    archivization_service_mock.archive.assert_called_with(ProjectID(123))


def test_unarchive_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.put("/projects/124/unarchive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    archivization_service_mock.unarchive.assert_called_with(ProjectID(124))


def test_delete_project_endpoint(container: Container, client: TestClient):
    # Given
    archivization_service_mock = Mock(spec=ArchivizationService)

    # When
    with container.archivization_service.override(archivization_service_mock):
        response = client.delete("/projects/124")

    # Then
    assert response.status_code == status.HTTP_200_OK
    archivization_service_mock.delete.assert_called_with(ProjectID(124))
