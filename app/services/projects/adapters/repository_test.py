import pytest

from app.services.projects.adapters.repository import Repository
from app.services.projects.domain.entities import Project
from app.services.projects.domain.errors import ProjectNotFoundError


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

    with pytest.raises(ProjectNotFoundError):
        repository.get(1)


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
