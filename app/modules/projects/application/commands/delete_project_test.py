from app.modules.projects.application.commands import DeleteProject, DeleteProjectHandler
from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.projects.domain.project_builder import ProjectBuilder
from app.utc_datetime import utc_datetime


def test_delete_project(
    repository: FakeProjectRepository,
    fake_uow: FakeUnitOfWork,
):
    # Given
    project = repository.create(ProjectBuilder().build())
    project.archive(now=utc_datetime(2021, 1, 1, 0, 0, 0))
    now = utc_datetime(2022, 1, 1, 0, 0, 0)

    # When
    handler = DeleteProjectHandler(uow=fake_uow)
    handler(DeleteProject(project_id=project.id, now=now))

    # Then
    assert fake_uow.committed is True
