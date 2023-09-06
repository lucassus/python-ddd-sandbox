from app.modules.projects.application.commands import ArchiveProject, ArchiveProjectHandler
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_datetime


def test_archive_project(
    repository: FakeProjectRepository,
    fake_uow: FakeUnitOfWork,
):
    # Given
    project = repository.create(ProjectBuilder().build())
    now = utc_datetime(2021, 1, 1, 0, 0, 0)

    # When
    handler = ArchiveProjectHandler(uow=fake_uow)
    handler(ArchiveProject(project_id=project.id, now=now))

    # Then
    assert fake_uow.committed is True
    assert project.archived is True
    assert project.archived_at == now
