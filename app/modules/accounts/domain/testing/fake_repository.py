from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.user import User


class FakeRepository(AbstractRepository):
    _users_by_id: dict[int, User]

    def __init__(self):
        self._users_by_id = {}

    def create(self, user: User) -> User:
        user.id = self._get_next_id()
        self._users_by_id[user.id] = user

        return user

    def exists_by_email(self, email: EmailAddress) -> bool:
        return any(user.email == email for user in self._users_by_id.values())

    def get(self, user_id: int) -> User | None:
        return self._users_by_id.get(user_id)

    def _get_next_id(self) -> int:
        return max(self._users_by_id.keys(), default=0) + 1
