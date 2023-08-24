from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


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

    def get_by_email(self, email: EmailAddress) -> User | None:
        for user in self._users_by_id.values():
            if user.email == email:
                return user

        return None

    def _get_next_id(self) -> UserID:
        return UserID.generate()
