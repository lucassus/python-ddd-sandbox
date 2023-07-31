import pytest

from app.command.accounts.use_cases.ports import AbstractRepository
from app.command.accounts.use_cases.testing import FakeRepository, FakeUnitOfWork
from app.shared_kernel.message_bus import MessageBus


@pytest.fixture
def repository() -> AbstractRepository:
    return FakeRepository()


@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture
def uow(repository: AbstractRepository):
    return FakeUnitOfWork(repository)
