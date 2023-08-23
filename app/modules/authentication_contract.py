import abc
from dataclasses import dataclass

from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class AuthenticationError(Exception):
    pass


class AuthenticationContract(metaclass=abc.ABCMeta):
    @dataclass(frozen=True)
    class CurrentUserDTO:
        id: UserID
        email: EmailAddress

    @abc.abstractmethod
    def trade_token_for_user(self, token: str) -> CurrentUserDTO:
        raise NotImplementedError
