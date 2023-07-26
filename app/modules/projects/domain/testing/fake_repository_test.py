import pytest

from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.testing.factories import build_project
from app.modules.projects.domain.testing.fake_repository import FakeRepository


def test_fake_repository():
    repository = FakeRepository()

    repository.create(build_project(name="First"))
    repository.create(build_project(name="Second"))

    project = repository.get(1)
    assert project is not None
    assert project.id == 1
    assert project.name == "First"

    with pytest.raises(ProjectNotFoundError):
        repository.get(3)
