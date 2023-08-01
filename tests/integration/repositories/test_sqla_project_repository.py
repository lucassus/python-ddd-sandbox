from datetime import date

import pytest

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.command.accounts.infrastructure.adapters.sqla_user_repository import SQLAUserRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.factories import build_project
from app.command.projects.entities.project import ProjectID
from app.command.projects.infrastructure.adapters.sqla_project_repository import SQLAProjectRepository

# TODO: Refactor to class TestSQLAProjectRepository


@pytest.fixture
def user(session):
    repository = SQLAUserRepository(session=session)

    user = repository.create(
        User(
            email=EmailAddress("test@email.com"),
            password=Password("password"),
        )
    )
    session.commit()

    return user


@pytest.fixture
def repository(session):
    return SQLAProjectRepository(session=session)


def test_sql_project_repository_get(session, user, repository: SQLAProjectRepository):
    # Given
    project = repository.create(build_project(user_id=user.id, name="Test project"))
    session.commit()

    # When
    loaded = repository.get(project.id)

    # Then
    assert loaded.name == "Test project"


def test_sql_project_repository_get_raises_error_when_not_found(session, repository: SQLAProjectRepository):
    with pytest.raises(ProjectNotFoundError):
        repository.get(ProjectID(1))


def test_sql_project_repository_get_raises_error_when_archived(session, user, repository: SQLAProjectRepository):
    # Given
    project = build_project(user_id=user.id, name="Test project")
    project.archive(date.today())
    project = repository.create(project)
    session.commit()

    # Then
    with pytest.raises(ProjectNotFoundError):
        repository.get(project.id)
