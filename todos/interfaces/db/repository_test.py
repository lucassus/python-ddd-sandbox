import pytest

from todos.domain.models import Project
from todos.interfaces.db.repository import Repository


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

    project = Project(name="One")
    session.add(project)

    project = Project(name="Two")
    session.add(project)

    session.commit()

    assert len(repository.list()) == 2
