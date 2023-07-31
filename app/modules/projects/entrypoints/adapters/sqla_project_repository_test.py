import pytest

from app.infrastructure.factories import create_project
from app.modules.projects.entities.errors import ProjectNotFoundError
from app.modules.projects.entities.project import ProjectID
from app.modules.projects.entrypoints.adapters.sqla_project_repository import SQLAProjectRepository


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
