import pytest

from app.infrastructure.message_bus import MessageBus
from app.modules.accounts.application.ports.tracking_user_repository import TrackingUserRepository
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.application.testing.fake_user_repository import FakeUserRepository


@pytest.fixture()
def repository():
    return FakeUserRepository()


@pytest.fixture()
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture()
def uow(repository: FakeUserRepository, message_bus: MessageBus):
    return FakeUnitOfWork(repository=TrackingUserRepository(repository), bus=message_bus)
