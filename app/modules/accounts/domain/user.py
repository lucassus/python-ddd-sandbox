from dataclasses import dataclass

from app.modules.accounts.domain.password import Password
from app.modules.shared_kernel.entities.aggregate_root import AggregateRoot
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import Event


class User(AggregateRoot):
    @dataclass(frozen=True)
    class AccountCreated(Event):
        user_id: UserID

    _id: UserID
    _email: EmailAddress
    _password: Password

    # TODO: Make it private
    events: list[Event]

    def __init__(
        self,
        id: UserID,
        email: EmailAddress,
        password: Password,
    ):
        self._id = id
        self._email = email
        self._password = password

        self.events = [self.AccountCreated(user_id=id)]

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

    def __hash__(self):
        return hash(self._id)
