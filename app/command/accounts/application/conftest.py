import pytest

from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.command.shared_kernel.message_bus import MessageBus


@pytest.fixture
def repository() -> AbstractUserRepository:
    return FakeUserRepository()


@pytest.fixture
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture
def uow(repository: AbstractUserRepository):
    return FakeUnitOfWork(repository)
