from unittest.mock import Mock

import pytest

from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.register_user import RegisterUser
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


@pytest.fixture()
def register_user(uow: FakeUnitOfWork, message_bus):
    return RegisterUser(uow=uow, bus=message_bus)


def test_register_user_creates_a_user(
    uow,
    register_user: RegisterUser,
):
    # When
    register_user(
        user_id=UserID.generate(),
        email=EmailAddress("test@email.com"),
        password=Password("passwd123"),
    )

    # Then
    assert uow.committed is True
    assert uow.user.exists_by_email(EmailAddress("test@email.com")) is True


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
    user_id = UserID.generate()
    register_user(
        user_id=user_id,
        email=EmailAddress("test@email.com"),
        password=Password("passwd123"),
    )

    # Then
    listener_mock.assert_called_once_with(User.AccountCreatedEvent(user_id=user_id))
    assert uow.committed is True


def test_register_user_validate_email_uniqueness(
    uow,
    repository: AbstractUserRepository,
    register_user: RegisterUser,
):
    existing_user = UserBuilder().with_email("existing@email.com").build()
    repository.create(existing_user)

    # Then
    with pytest.raises(
        EmailAlreadyExistsException,
        match="A user with the email existing@email.com already exists",
    ):
        register_user(
            user_id=UserID.generate(),
            email=EmailAddress("existing@email.com"),
            password=Password("passwd123"),
        )

    assert uow.committed is False
