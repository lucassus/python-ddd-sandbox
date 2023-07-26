from unittest.mock import Mock

import pytest

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.testing import FakeUnitOfWork, build_user
from app.modules.accounts.domain.use_cases import RegisterUser
from app.modules.accounts.domain.user import User


@pytest.fixture
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
    repository: AbstractRepository,
    register_user: RegisterUser,
):
    repository.create(build_user(email=EmailAddress("existing@email.com")))

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
