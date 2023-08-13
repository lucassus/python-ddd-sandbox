import pytest

from app.modules.projects.application.testing.fake_project_repository import FakeProjectRepository
from app.modules.projects.application.testing.fake_unit_of_work import FakeUnitOfWork


@pytest.fixture()
def repository():
    return FakeProjectRepository()


@pytest.fixture()
def fake_uow(repository):
    return FakeUnitOfWork(repository)
