from datetime import datetime

import pytest

from app.command.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.command.projects.entities.errors import ProjectNotFoundError
from app.command.projects.entities.project import Project, ProjectID
from app.command.shared_kernel.user_id import UserID


def test_fake_project_repository():
    repository = FakeProjectRepository()

    repository.create(Project(user_id=UserID(1), name="First"))
    repository.create(Project(user_id=UserID(1), name="Second"))

    project = repository.get(ProjectID(1))
    assert project is not None
    assert project.id == 1
    assert project.name == "First"

    with pytest.raises(
        ProjectNotFoundError,
        match="Unable to find Project with id=3",
    ):
        repository.get(ProjectID(3))

    archived_project = Project(user_id=UserID(1), name="Third")
    archived_project.archive(now=datetime.now())

    repository.create(archived_project)
    assert repository.get_archived(archived_project.id) is not None
