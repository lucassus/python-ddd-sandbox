from datetime import datetime

import pytest

from app.command.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.factories import build_project
from app.command.projects.entities.project import ProjectID


def test_fake_project_repository():
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

    archived_project = build_project(name="Third")
    archived_project.archived_at = datetime.now()
    repository.create(archived_project)
    assert repository.get_archived(archived_project.id) is not None
