import pytest

from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.modules.accounts.application.tracking_user_repository import TrackingUserRepository
from app.shared.message_bus import MessageBus


@pytest.fixture()
def repository():
    return FakeUserRepository()


@pytest.fixture()
def message_bus() -> MessageBus:
    return MessageBus()


@pytest.fixture()
def uow(repository: FakeUserRepository, message_bus: MessageBus):
    return FakeUnitOfWork(repository=TrackingUserRepository(repository), bus=message_bus)
