import pytest

from todos.adapters.db.repository import Repository
from todos.domain.entities import Project


@pytest.mark.integration
def test_repository_get(session):
    project = Project(name="Test project")
    session.add(project)
    session.commit()

    repository = Repository(session=session)
    assert repository.get(1) == project


@pytest.mark.integration
def test_repository_get_returns_none(session):
    repository = Repository(session=session)
    assert repository.get(1) is None


@pytest.mark.integration
def test_repository_list(session):
    repository = Repository(session=session)

    assert repository.list() == []

    project = Project(name="Project One")
    session.add(project)

    project = Project(name="Project Two")
    session.add(project)

    session.commit()

    assert len(repository.list()) == 2
