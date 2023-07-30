import pytest

from app.modules.projects.use_cases.testing import FakeRepository, FakeUnitOfWork


@pytest.fixture
def repository():
    return FakeRepository()


@pytest.fixture
def fake_uow(repository):
    return FakeUnitOfWork(repository)
