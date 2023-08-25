from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class FakeUserRepository(AbstractUserRepository):
    _users_by_id: dict[UserID, User]
    seen: set[User]

    def __init__(self):
        super().__init__()

        self._users_by_id = {}
        self.seen = set()

    def create(self, user: User) -> User:
        self._users_by_id[user.id] = user
        self.seen.add(user)

        return user

    def exists_by_email(self, email: EmailAddress) -> bool:
        return any(user.email == email for user in self._users_by_id.values())

    def get(self, user_id: UserID) -> User | None:
        user = self._users_by_id.get(user_id)

        # TODO: Dry it
        if user is not None:
            self.seen.add(user)

        return user

    def get_by_email(self, email: EmailAddress) -> User | None:
        for user in self._users_by_id.values():
            if user.email == email:
                self.seen.add(user)  # TODO: Dry it
                return user

        return None
