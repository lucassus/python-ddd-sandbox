import pytest

from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.domain.errors import ProjectNotFoundError
from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_now


def test_fake_project_repository():
    repository = FakeProjectRepository()

    repository.create(ProjectBuilder().with_name("First").build())
    repository.create(ProjectBuilder().with_name("Second").build())

    project = repository.get(ProjectID(1))
    assert project is not None
    assert project.id == 1
    assert project.name == "First"

    with pytest.raises(
        ProjectNotFoundError,
        match="Unable to find Project with id=3",
    ):
        repository.get(ProjectID(3))

    archived_project = ProjectBuilder().with_name("Archived").build()
    archived_project.archive(now=utc_now())

    repository.create(archived_project)
    assert repository.get_archived(archived_project.id) is not None
