from datetime import datetime, timedelta

import jwt

from app.command.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.utc_datetime import utc_now


class AuthenticationError(Exception):
    pass


class Authentication:
    def __init__(self, uow: AbstractUnitOfWork, secret_auth_key: str):
        self._uow = uow
        self._secret_auth_key = secret_auth_key

    def login(
        self,
        email: EmailAddress,
        password: Password,
        now: datetime | None = None,
    ) -> str:
        if now is None:
            now = utc_now()

        with self._uow as uow:
            user = uow.user.get_by_email(email)

        if user is None:
            raise AuthenticationError()

        if user.password != password:
            raise AuthenticationError()

        return jwt.encode(
            payload={
                "sub": str(user.id),
                "exp": now + timedelta(days=90),
                "iat": now,
            },
            key=self._secret_auth_key,
            algorithm="HS256",
        )
