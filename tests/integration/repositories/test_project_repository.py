from datetime import date

import pytest

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.command.accounts.infrastructure.adapters.user_repository import UserRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.factories import build_project
from app.command.projects.entities.project import ProjectID
from app.command.projects.infrastructure.adapters.project_repository import ProjectRepository


class TestProjectRepository:
    @pytest.fixture
    def repository(self, session):
        return ProjectRepository(session=session)

    def test_get(self, session, create_user, repository: ProjectRepository):
        # Given
        user = create_user()
        project = repository.create(build_project(user_id=user.id, name="Test project"))
        session.commit()

        # When
        loaded = repository.get(project.id)

        # Then
        assert loaded.name == "Test project"

    def test_get_raises_error_when_not_found(self, session, repository: ProjectRepository):
        with pytest.raises(ProjectNotFoundError):
            repository.get(ProjectID(1))

    def test_get_raises_error_when_archived(self, session, create_user, repository: ProjectRepository):
        # Given
        user = create_user()
        project = build_project(user_id=user.id, name="Test project")
        project.archive(date.today())
        project = repository.create(project)
        session.commit()

        # Then
        with pytest.raises(ProjectNotFoundError):
            repository.get(project.id)

    def test_get_archived(self, session, create_user, repository: ProjectRepository):
        # Given
        user = create_user()
        project = build_project(user_id=user.id, name="Test project")
        project.archive(date.today())
        project = repository.create(project)
        session.commit()

        # When
        loaded = repository.get_archived(project.id)

        # Then
        assert loaded.name == "Test project"

    def test_get_archived_raises_error_when_not_found(self, session, repository: ProjectRepository):
        with pytest.raises(ProjectNotFoundError):
            repository.get_archived(ProjectID(1))

    def test_get_archived_raises_error_when_not_archived(self, session, create_user, repository: ProjectRepository):
        # Given
        user = create_user()
        project = build_project(user_id=user.id, name="Test project")
        project = repository.create(project)
        session.commit()

        # Then
        with pytest.raises(ProjectNotFoundError):
            repository.get_archived(project.id)
