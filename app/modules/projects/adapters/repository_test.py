import pytest

from app.modules.projects.adapters.repository import Repository
from app.modules.projects.domain.entities import Project
from app.modules.projects.domain.errors import ProjectNotFoundError


def test_repository_get(session):
    project = Project(name="Test project")
    session.add(project)
    session.commit()

    repository = Repository(session=session)
    assert repository.get(1) == project


def test_repository_get_returns_none(session):
    repository = Repository(session=session)

    with pytest.raises(ProjectNotFoundError):
        repository.get(1)


def test_repository_list(session):
    repository = Repository(session=session)

    assert repository.list() == []

    project = Project(name="Project One")
    session.add(project)

    project = Project(name="Project Two")
    session.add(project)

    session.commit()

    assert len(repository.list()) == 2
