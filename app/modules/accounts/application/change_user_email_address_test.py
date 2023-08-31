import pytest

from app.modules.accounts.application.change_user_email_address import ChangeUserEmailAddressCommandHandler
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException, UserNotFoundError
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


@pytest.fixture()
def change_user_email_address(uow: FakeUnitOfWork):
    return ChangeUserEmailAddressCommandHandler(uow=uow)


class TestChangeUserEmailAddressUseCase:
    def test_successfully_updates_user_email_address(
        self,
        repository: AbstractUserRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddressCommandHandler,
    ):
        # Given
        user = repository.create(UserBuilder().with_email("old@email.com").build())

        # When
        change_user_email_address(
            user_id=user.id,
            new_email=EmailAddress("new@email.com"),
        )

        # Then
        assert user.email == EmailAddress("new@email.com")
        assert uow.committed is True

    def test_raises_error_when_user_does_not_exist(
        self,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddressCommandHandler,
    ):
        with pytest.raises(UserNotFoundError):
            change_user_email_address(
                user_id=UserID.generate(),
                new_email=EmailAddress("new@email.com"),
            )

        assert uow.committed is False

    def test_raises_error_when_new_email_address_is_taken(
        self,
        repository: AbstractUserRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddressCommandHandler,
    ):
        # Given
        repository.create(UserBuilder().with_email("taken@email.com").build())
        user = repository.create(UserBuilder().with_email("old@email.com").build())

        # When
        with pytest.raises(EmailAlreadyExistsException):
            change_user_email_address(
                user_id=user.id,
                new_email=EmailAddress("taken@email.com"),
            )

        # Then
        assert uow.committed is False

    def test_does_nothing_when_new_email_address_is_the_same_as_the_old_one(
        self,
        repository: AbstractUserRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddressCommandHandler,
    ):
        # Given
        user = repository.create(UserBuilder().with_email("old@email.com").build())

        # When
        change_user_email_address(
            user_id=user.id,
            new_email=EmailAddress("old@email.com"),
        )

        # Then
        assert uow.committed is False
        assert user.email == EmailAddress("old@email.com")
