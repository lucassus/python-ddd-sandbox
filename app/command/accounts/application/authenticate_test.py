import pytest

from app.command.accounts.application.authenticate import Authenticate
from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user_builder import UserBuilder


class TestAuthenticate:
    @pytest.fixture()
    def authenticate(self, uow: FakeUnitOfWork):
        return Authenticate(uow=uow, secret_auth_key="test-secret")

    def test_on_success(self, repository: AbstractUserRepository, authenticate: Authenticate):
        repository.create(UserBuilder().with_email("test@email.com").with_password("secret-password").build())

        token = authenticate(
            EmailAddress("test@email.com"),
            Password("secret-password"),
        )

        assert isinstance(token, str)
