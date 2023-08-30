from dataclasses import dataclass

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
    _hashed_password: str

    def __init__(
        self,
        id: UserID,
        email: EmailAddress,
        hashed_password: str,
    ):
        super().__init__()

        self._id = id
        self._email = email
        self._hashed_password = hashed_password

        self.queue_event(User.AccountCreated(user_id=self._id))

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
    def hashed_password(self) -> str:
        return self._hashed_password

    def __hash__(self):
        return hash(self._id)
