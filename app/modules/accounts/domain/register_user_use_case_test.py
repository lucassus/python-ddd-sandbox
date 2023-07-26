from unittest.mock import Mock

import pytest

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.ports import AbstractRepository, AbstractUnitOfWork
from app.modules.accounts.domain.register_user_use_case import EmailAlreadyExistsException, RegisterUserUseCase
from app.modules.accounts.domain.user import User
from app.shared.message_bus import MessageBus


class FakeRepository(AbstractRepository):
    def exists_by_email(self, email: EmailAddress) -> bool:
        return email == EmailAddress("existing@email.com")

    def create(self, user: User):
        user.id = 123

    def get(self, user_id) -> User | None:
        return None


class FakeUnitOfWork(AbstractUnitOfWork):
    committed = False

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.fixture()
def uow():
    return FakeUnitOfWork(FakeRepository())


@pytest.fixture()
def message_bus():
    return MessageBus()


@pytest.fixture()
def register_user(uow, message_bus):
    return RegisterUserUseCase(uow=uow, bus=message_bus)


def test_register_user_returns_user_id(register_user: RegisterUserUseCase, uow):
    # When
    user_id = register_user(
        email=EmailAddress("test@email.com"),
        password=Password("passwd123"),
    )

    # Then
    assert user_id == 123
    assert uow.committed


def test_register_user_dispatches_account_created_event(uow, message_bus, register_user: RegisterUserUseCase):
    # Given
    listener_mock = Mock()
    message_bus.listen(User.AccountCreatedEvent, listener_mock)

    # When
    register_user(
        email=EmailAddress("test@email.com"),
        password=Password("passwd123"),
    )

    # Then
    listener_mock.assert_called_once_with(User.AccountCreatedEvent(user_id=123))
    assert uow.committed


def test_register_user_validate_email_uniqueness(uow, register_user: RegisterUserUseCase):
    # Then
    with pytest.raises(
        EmailAlreadyExistsException,
        match="A user with the email existing@email.com already exists",
    ):
        register_user(
            email=EmailAddress("existing@email.com"),
            password=Password("passwd123"),
        )

    assert not uow.committed
