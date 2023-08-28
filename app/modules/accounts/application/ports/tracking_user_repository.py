from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class TrackingUserRepository:
    _seen: set[User]

    def __init__(self, repository: AbstractUserRepository):
        self._repository = repository
        self._seen = set()

    @property
    def seen(self) -> frozenset[User]:
        return frozenset(self._seen)

    def create(self, user: User) -> User:
        user = self._repository.create(user)
        self._seen.add(user)
        return user

    def exists_by_email(self, email: EmailAddress) -> bool:
        return self._repository.exists_by_email(email)

    def get(self, user_id: UserID) -> User | None:
        user = self._repository.get(user_id)

        if user is not None:
            self._seen.add(user)

        return user

    def get_by_email(self, email: EmailAddress) -> User | None:
        user = self._repository.get_by_email(email)

        if user is not None:
            self._seen.add(user)

        return user
