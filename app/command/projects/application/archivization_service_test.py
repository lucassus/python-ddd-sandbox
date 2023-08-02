from datetime import datetime

import pytest

from app.command.projects.application.archivization_service import ArchivizationService
from app.command.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.command.projects.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.projects.entities.factories import build_project


class TestArchiveService:
    @pytest.fixture
    def fake_project_repository(self):
        return FakeProjectRepository()

    @pytest.fixture
    def fake_unit_of_work(self, fake_project_repository):
        return FakeUnitOfWork(repository=fake_project_repository)

    @pytest.fixture
    def service(self, fake_unit_of_work):
        return ArchivizationService(uow=fake_unit_of_work)

    def test_archive(
        self,
        fake_project_repository: FakeProjectRepository,
        service: ArchivizationService,
        fake_unit_of_work: FakeUnitOfWork,
    ):
        # Given
        project = fake_project_repository.create(build_project(name="Project 1"))

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
        project = fake_project_repository.create(build_project(name="Project 1", archived_at=datetime.now()))

        # When
        service.unarchive(project.id)

        # Then
        assert fake_unit_of_work.committed is True
        assert project.archived is False
