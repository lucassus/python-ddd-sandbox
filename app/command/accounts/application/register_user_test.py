from unittest.mock import Mock

import pytest

from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.register_user import RegisterUser
from app.command.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.errors import EmailAlreadyExistsException
from app.command.accounts.domain.password import Password
from app.command.accounts.domain.user import User
from app.command.accounts.domain.user_builder import UserBuilder


@pytest.fixture()
def register_user(uow: FakeUnitOfWork, message_bus):
    return RegisterUser(uow=uow, bus=message_bus)


def test_register_user_returns_user_id(
    uow,
    register_user: RegisterUser,
):
    # When
    user_id = register_user(email=EmailAddress("test@email.com"), password=Password("passwd123"))

    # Then
    assert isinstance(user_id, int)
    assert uow.committed is True


def test_register_user_dispatches_account_created_event(
    uow,
    message_bus,
    repository,
    register_user: RegisterUser,
):
    # Given
    listener_mock = Mock()
    message_bus.listen(User.AccountCreatedEvent, listener_mock)

    # When
    user_id = register_user(email=EmailAddress("test@email.com"), password=Password("passwd123"))

    # Then
    listener_mock.assert_called_once_with(User.AccountCreatedEvent(user_id=user_id))
    assert uow.committed is True


def test_register_user_validate_email_uniqueness(
    uow,
    repository: AbstractUserRepository,
    register_user: RegisterUser,
):
    repository.create(UserBuilder().with_email("existing@email.com").build())

    # Then
    with pytest.raises(
        EmailAlreadyExistsException,
        match="A user with the email existing@email.com already exists",
    ):
        register_user(
            email=EmailAddress("existing@email.com"),
            password=Password("passwd123"),
        )

    assert uow.committed is False
