import pytest

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import UserNotFoundError
from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.testing import FakeUnitOfWork, build_user
from app.modules.accounts.domain.use_cases import ChangeUserEmailAddress


@pytest.fixture
def change_user_email_address(uow: FakeUnitOfWork):
    return ChangeUserEmailAddress(uow=uow)


class TestChangeUserEmailAddressUseCase:
    def test_success(
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
                user_id=123,
                new_email=EmailAddress("new@email.com"),
            )

        assert uow.committed is False

    # TODO: What if the new email address is the same as the old one?
    def test_raises_error_when_new_email_address_is_taken(
        self,
        repository: AbstractRepository,
        uow: FakeUnitOfWork,
        change_user_email_address: ChangeUserEmailAddress,
    ):
        # Given
        repository.create(build_user(email=EmailAddress("taken@email.com")))

        with pytest.raises(Exception):
            change_user_email_address(
                user_id=123,
                new_email=EmailAddress("taken@email.com"),
            )

        assert uow.committed is False
