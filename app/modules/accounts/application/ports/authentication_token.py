import abc
from datetime import datetime, timedelta

from app.modules.shared_kernel.entities.user_id import UserID


class AuthenticationTokenError(Exception):
    pass


class AuthenticationToken(metaclass=abc.ABCMeta):
    _expiration_delta = timedelta(days=90)

    def __init__(self, secret_key: str):
        self._secret_key = secret_key

    @abc.abstractmethod
    def encode(self, user_id: UserID, now: datetime | None = None) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, token: str) -> UserID:
        raise NotImplementedError
