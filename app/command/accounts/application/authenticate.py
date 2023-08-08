import jwt

from app.command.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password


class AuthenticationError(Exception):
    pass


class Authenticate:
    def __init__(self, uow: AbstractUnitOfWork, secret_auth_key: str):
        self._uow = uow
        self._secret_auth_key = secret_auth_key

    def __call__(self, email: EmailAddress, password: Password) -> str:
        with self._uow as uow:
            user = uow.user.get_by_email(email)

            if user is None:
                raise AuthenticationError()

            if user.password != password:
                raise AuthenticationError()

            return jwt.encode(
                payload={"sub": str(user.id)},
                key=self._secret_auth_key,
                algorithm="HS256",
            )
