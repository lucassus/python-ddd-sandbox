import pytest

from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.testing import FakeRepository, FakeUnitOfWork
from app.shared.message_bus import MessageBus


@pytest.fixture
def repository() -> AbstractRepository:
    return FakeRepository()


@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture
def uow(repository: AbstractRepository):
    return FakeUnitOfWork(repository)
