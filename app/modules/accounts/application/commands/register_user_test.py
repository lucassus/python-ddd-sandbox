import pytest

from app.modules.accounts.application.commands import RegisterUser, RegisterUserHandler
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.testing.fake_password_hasher import FakePasswordHasher
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.email_address import EmailAddress


@pytest.fixture
def register_user(uow: FakeUnitOfWork, message_bus):
    return RegisterUserHandler(uow=uow, password_hasher=FakePasswordHasher())


def test_register_user_creates_a_user(
    uow: FakeUnitOfWork,
    register_user: RegisterUserHandler,
):
    # When
    user_id = register_user(
        RegisterUser(
            email=EmailAddress("test@email.com"),
            password=Password("passwd123"),
        )
    )

    # Then
    assert uow.committed is True
    user = uow.users.get_by_email(EmailAddress("test@email.com"))
    assert user is not None
    assert user.email == EmailAddress("test@email.com")
    assert isinstance(user.hashed_password, str)
    assert user.id == user_id


def test_register_user_validate_email_uniqueness(
    uow,
    repository: AbstractUserRepository,
    register_user: RegisterUserHandler,
):
    existing_user = UserBuilder().with_email("existing@email.com").build()
    repository.create(existing_user)

    # Then
    with pytest.raises(
        EmailAlreadyExistsException,
        match="A user with the email existing@email.com already exists",
    ):
        register_user(
            RegisterUser(
                email=EmailAddress("existing@email.com"),
                password=Password("passwd123"),
            )
        )

    assert uow.committed is False
