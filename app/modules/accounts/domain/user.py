from app.modules.shared_kernel.entities.aggregate_root import AggregateRoot
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.events import UserAccountCreated


class User(AggregateRoot):
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

        self.queue_event(UserAccountCreated(user_id=self._id))

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
