import pytest

from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.entities.errors import ProjectNotFoundError
from app.modules.projects.entities.factories import build_project
from app.modules.projects.entities.project import ProjectID


def test_fake_repository():
    repository = FakeProjectRepository()

    repository.create(build_project(name="First"))
    repository.create(build_project(name="Second"))

    project = repository.get(ProjectID(1))
    assert project is not None
    assert project.id == 1
    assert project.name == "First"

    with pytest.raises(
        ProjectNotFoundError,
        match="Unable to find Project with id=3",
    ):
        repository.get(ProjectID(3))
