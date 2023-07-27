import pytest

from app.modules.projects.domain.testing import FakeRepository, FakeUnitOfWork


@pytest.fixture
def repository():
    return FakeRepository()


@pytest.fixture
def fake_uow(repository):
    return FakeUnitOfWork(repository)
