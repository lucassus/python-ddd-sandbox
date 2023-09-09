from app.modules.projects.application.commands import UnarchiveProject, UnarchiveProjectHandler
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_now


def test_unarchive_project(
    repository: FakeProjectRepository,
    fake_uow: FakeUnitOfWork,
):
    # Given
    project = repository.create(ProjectBuilder().build())
    project.archive(now=utc_now())

    # When
    handler = UnarchiveProjectHandler(uow=fake_uow)
    handler(UnarchiveProject(project_id=project.id))

    # Then
    assert fake_uow.committed is True
    assert project.archived is False
