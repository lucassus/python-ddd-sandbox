from dataclasses import dataclass

from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.password import Password
from app.command.shared_kernel.entities.aggregate_root import AggregateRoot
from app.command.shared_kernel.entities.user_id import UserID
from app.command.shared_kernel.message_bus import BaseEvent


class User(AggregateRoot):
    @dataclass(frozen=True)
    class AccountCreatedEvent(BaseEvent):
        user_id: UserID

    _id: UserID
    _email: EmailAddress
    _password: Password

    def __init__(
        self,
        email: EmailAddress,
        password: Password,
    ):
        self._email = email
        self._password = password

    @property
    def id(self) -> UserID:
        return self._id

    @property
    def email(self) -> EmailAddress:
        return self._email

    @email.setter
    def email(self, email: EmailAddress) -> None:
        self._email = email

    @property
    def password(self) -> Password:
        return self._password
