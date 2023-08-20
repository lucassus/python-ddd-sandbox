from datetime import datetime

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.ports.authenticationtoken import AuthenticationToken, AuthenticationTokenError
from app.modules.accounts.domain.password import Password
from app.modules.authentication_contract import AuthenticationContract, AuthenticationError
from app.modules.shared_kernel.entities.email_address import EmailAddress


class Authentication(AuthenticationContract):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        auth_token: AuthenticationToken,
    ):
        self._uow = uow
        self._auth_token = auth_token

    def login(
        self,
        email: EmailAddress,
        password: Password,
        now: datetime | None = None,
    ) -> str:
        with self._uow as uow:
            user = uow.user.get_by_email(email)

            if user is None or user.password != password:
                raise AuthenticationError()

            return self._auth_token.encode(user.id, now)

    def trade_token_for_user(self, token: str) -> AuthenticationContract.CurrentUserDTO:
        try:
            user_id = self._auth_token.decode(token)
        except AuthenticationTokenError as e:
            raise AuthenticationError() from e

        with self._uow as uow:
            user = uow.user.get(user_id)

            if user is None:
                raise AuthenticationError()

            return AuthenticationContract.CurrentUserDTO(
                id=user.id,
                email=user.email,
            )
