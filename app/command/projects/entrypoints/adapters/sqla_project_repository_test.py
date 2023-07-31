import pytest

from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import ProjectID
from app.command.projects.entrypoints.adapters.sqla_project_repository import SQLAProjectRepository
from app.infrastructure.factories import create_project


def test_repository_get(session):
    project_id = create_project(session.connection(), name="Test project").id

    repository = SQLAProjectRepository(session=session)
    project = repository.get(ProjectID(1))

    assert project.id == project_id
    assert project.name == "Test project"


def test_repository_get_returns_none(session):
    repository = SQLAProjectRepository(session=session)

    with pytest.raises(ProjectNotFoundError):
        repository.get(ProjectID(1))
