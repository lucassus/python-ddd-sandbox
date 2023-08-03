from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.user import User
from app.command.shared_kernel.user_id import UserID


class FakeUserRepository(AbstractUserRepository):
    _users_by_id: dict[UserID, User]

    def __init__(self):
        self._users_by_id = {}

    def create(self, user: User) -> User:
        user._id = self._get_next_id()
        self._users_by_id[user.id] = user

        return user

    def exists_by_email(self, email: EmailAddress) -> bool:
        return any(user.email == email for user in self._users_by_id.values())

    def get(self, user_id: UserID) -> User | None:
        return self._users_by_id.get(user_id)

    def _get_next_id(self) -> UserID:
        return UserID(max(self._users_by_id.keys(), default=0) + 1)
