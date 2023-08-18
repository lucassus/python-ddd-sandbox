import abc
from dataclasses import dataclass
from typing import Protocol

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class AuthenticationError(Exception):
    pass


class AuthenticationContract(metaclass=abc.ABCMeta):
    @dataclass(frozen=True)
    class UserDTO:
        id: UserID
        email: EmailAddress

    @abc.abstractmethod
    def trade_token_for_user(self, token: str) -> UserDTO:
        raise NotImplementedError()
