import pytest

from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import ProjectID
from app.command.projects.infrastructure.adapters.project_repository import ProjectRepository
from app.utc_datetime import utc_now


class TestProjectRepository:
    @pytest.fixture()
    def repository(self, session):
        return ProjectRepository(session=session)

    def test_get(self, session, create_project, repository: ProjectRepository):
        # Given
        project = create_project(name="Test project")
        session.commit()

        # When
        loaded = repository.get_active(project.id)

        # Then
        assert loaded.name == "Test project"

    def test_get_raises_error_when_not_found(self, session, repository: ProjectRepository):
        with pytest.raises(ProjectNotFoundError):
            repository.get_active(ProjectID(1))

    def test_get_raises_error_when_archived(self, session, create_project, repository: ProjectRepository):
        # Given
        project = create_project()
        project.archive(now=utc_now())
        session.commit()

        # Then
        with pytest.raises(ProjectNotFoundError):
            repository.get_active(project.id)

    def test_get_archived(self, session, create_project, repository: ProjectRepository):
        # Given
        project = create_project()
        project.archive(now=utc_now())
        session.commit()

        # When
        loaded = repository.get_archived(project.id)

        # Then
        assert loaded.name == "Test project"

    def test_get_archived_raises_error_when_not_found(self, session, repository: ProjectRepository):
        with pytest.raises(ProjectNotFoundError):
            repository.get_archived(ProjectID(1))

    def test_get_archived_raises_error_when_deleted(self, session, create_project, repository: ProjectRepository):
        # Given
        project = create_project()
        project.archive(now=utc_now())
        project.delete(now=utc_now())
        session.commit()

        # Then
        with pytest.raises(ProjectNotFoundError):
            repository.get_archived(project.id)

    def test_get_archived_raises_error_when_not_archived(self, session, create_project, repository: ProjectRepository):
        # Given
        project = create_project()
        session.commit()

        # Then
        with pytest.raises(ProjectNotFoundError):
            repository.get_archived(project.id)
