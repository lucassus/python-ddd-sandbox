from unittest.mock import Mock

from app.modules.accounts.domain.entities import User
from app.modules.accounts.domain.ports import AbstractRepository, AbstractUnitOfWork
from app.modules.accounts.domain.service import Service
from app.shared.message_bus import MessageBus


class FakeRepository(AbstractRepository):
    def create(self, user: User):
        user.id = 123


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.repository = FakeRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


def test_register_user_returns_user_id():
    # Given
    service = Service(uow=FakeUnitOfWork(), bus=(MessageBus()))

    # When
    user_id = service.register_user(email="test@email.com", password="passwd123")

    # Then
    assert user_id == 123


def test_register_user_dispatches_account_created_event():
    # Given
    listener_mock = Mock()
    message_bus = MessageBus()
    message_bus.listen(User.AccountCreatedEvent, listener_mock)

    service = Service(uow=FakeUnitOfWork(), bus=message_bus)

    # When
    service.register_user(email="test@email.com", password="passwd123")

    # Then
    listener_mock.assert_called_once_with(User.AccountCreatedEvent(user_id=123))


def test_register_user_validate_email_uniqueness():
    pass
