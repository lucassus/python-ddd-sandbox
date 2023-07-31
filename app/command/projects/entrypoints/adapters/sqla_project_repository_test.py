from datetime import date

import pytest

from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import ProjectID
from app.command.projects.entrypoints.adapters.sqla_project_repository import SQLAProjectRepository
from app.infrastructure.factories import create_project


@pytest.fixture
def repository(session):
    return SQLAProjectRepository(session=session)


def test_sql_project_repository_get(session, repository: SQLAProjectRepository):
    project_id = create_project(session.connection(), name="Test project").id

    project = repository.get(ProjectID(project_id))

    assert project.id == project_id
    assert project.name == "Test project"


def test_sql_project_repository_get_raises_error_when_not_found(session, repository: SQLAProjectRepository):
    with pytest.raises(ProjectNotFoundError):
        repository.get(ProjectID(1))


def test_sql_project_repository_get_raises_error_when_archived(session, repository: SQLAProjectRepository):
    project_id = create_project(session.connection(), name="Test project", archived_at=date.today()).id

    with pytest.raises(ProjectNotFoundError):
        repository.get(ProjectID(project_id))
