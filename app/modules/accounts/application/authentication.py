from dataclasses import dataclass
from datetime import datetime

from app.modules.accounts.application.jwt import JWT, JWTError
from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.shared_kernel.entities.user_id import UserID


class AuthenticationError(Exception):
    pass


class Authentication:
    @dataclass(frozen=True)
    class UserDTO:
        id: UserID
        email: EmailAddress

    def __init__(self, uow: AbstractUnitOfWork, jwt: JWT):
        self._uow = uow
        self._jwt = jwt

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

            return self._jwt.encode(user.id, now)

    def trade_token_for_user(self, token: str) -> UserDTO:
        try:
            user_id = self._jwt.decode(token)
        except JWTError as e:
            raise AuthenticationError() from e

        with self._uow as uow:
            user = uow.user.get(user_id)

            if user is None:
                raise AuthenticationError()

            return Authentication.UserDTO(
                id=user.id,
                email=user.email,
            )
