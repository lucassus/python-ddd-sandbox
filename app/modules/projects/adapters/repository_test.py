import pytest

from app.infrastructure.factories import create_project
from app.modules.projects.adapters.repository import Repository
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.project import ProjectID


def test_repository_get(session):
    project_id = create_project(session.connection(), name="Test project").id

    repository = Repository(session=session)
    project = repository.get(ProjectID(1))

    assert project.id == project_id
    assert project.name == "Test project"


def test_repository_get_returns_none(session):
    repository = Repository(session=session)

    with pytest.raises(ProjectNotFoundError):
        repository.get(ProjectID(1))
