import pytest

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.command.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.projects.entities.project_builder import ProjectBuilder
from app.utc_datetime import utc_now


class TestArchiveService:
    @pytest.fixture()
    def fake_project_repository(self):
        return FakeProjectRepository()

    @pytest.fixture()
    def fake_unit_of_work(self, fake_project_repository):
        return FakeUnitOfWork(repository=fake_project_repository)

    @pytest.fixture()
    def service(self, fake_unit_of_work):
        return ArchivizationService(uow=fake_unit_of_work)

    def test_archive(
        self,
        fake_project_repository: FakeProjectRepository,
        service: ArchivizationService,
        fake_unit_of_work: FakeUnitOfWork,
    ):
        # Given
        project = fake_project_repository.create(ProjectBuilder().build())

        # When
        service.archive(project.id)

        # Then
        assert fake_unit_of_work.committed is True
        assert project.archived is True

    def test_unarchive(
        self,
        fake_project_repository: FakeProjectRepository,
        service: ArchivizationService,
        fake_unit_of_work: FakeUnitOfWork,
    ):
        # Given
        project = fake_project_repository.create(ProjectBuilder().build())
        project.archive(now=utc_now())

        # When
        service.unarchive(project.id)

        # Then
        assert fake_unit_of_work.committed is True
        assert project.archived is False
