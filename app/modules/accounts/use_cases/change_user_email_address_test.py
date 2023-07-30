import pytest

from app.modules.accounts.domain import EmailAddress, EmailAlreadyExistsException, UserNotFoundError
from app.modules.accounts.use_cases import ChangeUserEmailAddress
from app.modules.accounts.use_cases.ports import AbstractRepository
from app.modules.accounts.use_cases.testing import FakeUnitOfWork, build_user
from app.shared_kernel.user_id import UserID


@pytest.fixture
def change_user_email_address(uow: FakeUnitOfWork):
    return ChangeUserEmailAddress(uow=uow)


class TestChangeUserEmailAddressUseCase:
    def test_successfully_updates_user_email_address(
        self,
        repository: AbstractRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddress,
    ):
        # Given
        user = repository.create(build_user(email=EmailAddress("old@email.com")))

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
        repository: AbstractRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddress,
    ):
        with pytest.raises(UserNotFoundError):
            change_user_email_address(
                user_id=UserID(123),
                new_email=EmailAddress("new@email.com"),
            )

        assert uow.committed is False

    def test_raises_error_when_new_email_address_is_taken(
        self,
        repository: AbstractRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddress,
    ):
        # Given
        repository.create(build_user(email=EmailAddress("taken@email.com")))
        user = repository.create(build_user(email=EmailAddress("old@email.com")))

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
        repository: AbstractRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddress,
    ):
        # Given
        user = repository.create(build_user(email=EmailAddress("old@email.com")))

        # When
        change_user_email_address(
            user_id=user.id,
            new_email=EmailAddress("old@email.com"),
        )

        # Then
        assert uow.committed is False
        assert user.email == EmailAddress("old@email.com")
