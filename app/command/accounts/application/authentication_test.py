import pytest

from app.command.accounts.application.authentication import Authentication
from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user_builder import UserBuilder


class TestAuthenticate:
    @pytest.fixture()
    def authentication(self, uow: FakeUnitOfWork):
        return Authentication(uow=uow, secret_auth_key="test-secret")

    def test_on_success(self, repository: AbstractUserRepository, authentication: Authentication):
        # Given
        user = UserBuilder().with_email("test@email.com").with_password("secret-password").build()
        repository.create(user)

        # When
        token = authentication.login(user.email, user.password)

        # Then
        assert isinstance(token, str)
