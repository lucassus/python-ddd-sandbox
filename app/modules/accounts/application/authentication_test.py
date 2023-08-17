import pytest

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.jwt import JWT
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.user_builder import UserBuilder


class TestAuthenticate:
    @pytest.fixture()
    def authentication(self, uow: FakeUnitOfWork):
        return Authentication(uow=uow, jwt=JWT(jwt_secret_key="test-secret"))

    def test_login_on_success(self, repository: AbstractUserRepository, authentication: Authentication):
        # Given
        user = UserBuilder().with_email("test@email.com").with_password("secret-password").build()
        repository.create(user)

        # When
        token = authentication.login(user.email, user.password)

        # Then
        assert isinstance(token, str)

    def test_trade_token_for_user(self, repository: AbstractUserRepository, authentication: Authentication):
        # Given
        user = UserBuilder().build()
        repository.create(user)
        token = authentication.login(user.email, user.password)

        # When
        user_dto = authentication.trade_token_for_user(token)

        # Then
        assert user_dto.id == user.id
        assert user_dto.email == user.email
