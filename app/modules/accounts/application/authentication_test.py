from datetime import datetime
from typing import Optional

import pytest

from app.modules.accounts.application.authentication import Authentication
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.ports.authentication_token import AuthenticationToken
from app.modules.accounts.application.testing.fake_password_hasher import FakePasswordHasher
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.user_id import UserID


class FakeAuthenticationToken(AuthenticationToken):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    def encode(self, user_id: UserID, now: Optional[datetime] = None) -> str:
        return f"token-{self._secret_key}-{user_id}"

    def decode(self, token: str) -> UserID:
        return UserID(token.replace(f"token-{self._secret_key}-", ""))


class TestAuthenticate:
    @pytest.fixture
    def authentication(self, uow: FakeUnitOfWork):
        return Authentication(
            uow=uow,
            token=FakeAuthenticationToken(secret_key="test-secret"),
            password_hasher=FakePasswordHasher(),
        )

    def test_login_on_success(self, repository: AbstractUserRepository, authentication: Authentication):
        # Given
        password = Password("secret-password")
        user = UserBuilder().with_email("test@email.com").with_password(password).build()
        repository.create(user)

        # When
        token = authentication.login(user.email, password)

        # Then
        assert isinstance(token, str)

    def test_trade_token_for_user(self, repository: AbstractUserRepository, authentication: Authentication):
        # Given
        password = Password("passwd123")
        user = UserBuilder().with_password(password).build()
        repository.create(user)
        token = authentication.login(user.email, password)

        # When
        user_dto = authentication.trade_token_for_user(token)

        # Then
        assert user_dto.id == user.id
        assert user_dto.email == user.email
