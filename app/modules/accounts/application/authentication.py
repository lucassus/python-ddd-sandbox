from datetime import datetime, timedelta

import jwt

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


class AuthenticationError(Exception):
    pass


JWT_ENCODE_ALGORITHM = "HS256"


class Authentication:
    def __init__(self, uow: AbstractUnitOfWork, jwt_secret_key: str):
        self._uow = uow
        self._jwt_secret_key = jwt_secret_key

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
            user_id, user_password = user.id, user.password

        if user is None or user_password != password:
            raise AuthenticationError()

        return jwt.encode(
            payload={
                "sub": user_id,
                "exp": now + timedelta(days=90),
                "iat": now,
            },
            key=self._jwt_secret_key,
            algorithm=JWT_ENCODE_ALGORITHM,
        )

    def trade_token_for_user(self, token: str) -> User:
        payload = jwt.decode(
            token,
            key=self._jwt_secret_key,
            algorithms=[JWT_ENCODE_ALGORITHM],
        )

        user_id = UserID(payload["sub"])

        with self._uow as uow:
            user = uow.user.get(user_id)

        if user is None:
            raise AuthenticationError()

        return user
