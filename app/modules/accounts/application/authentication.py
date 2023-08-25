from datetime import datetime

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.ports.authentication_token import AuthenticationToken, AuthenticationTokenError
from app.modules.accounts.domain.password import Password
from app.modules.authentication_contract import AuthenticationContract, AuthenticationError
from app.modules.shared_kernel.entities.email_address import EmailAddress


class Authentication(AuthenticationContract):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        token: AuthenticationToken,
    ):
        self._uow = uow
        self._token = token

    def login(
        self,
        email: EmailAddress,
        password: Password,
        now: datetime | None = None,
    ) -> str:
        with self._uow as uow:
            user = uow.users.get_by_email(email)

            if user is None or user.password != password:
                raise AuthenticationError("Invalid email or password")  # noqa: TRY003

            return self._token.encode(user.id, now)

    def trade_token_for_user(self, token: str) -> AuthenticationContract.CurrentUserDTO:
        try:
            user_id = self._token.decode(token)
        except AuthenticationTokenError as e:
            raise AuthenticationError() from e

        with self._uow as uow:
            user = uow.users.get(user_id)
            uow.commit()

        if user is None:
            raise AuthenticationError()

        return AuthenticationContract.CurrentUserDTO(
            id=user.id,
            email=user.email,
        )
