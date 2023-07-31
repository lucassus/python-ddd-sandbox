import abc

from app.command.accounts.domain import EmailAddress, User
from app.shared_kernel.user_id import UserID


class AbstractRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def exists_by_email(self, email: EmailAddress) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id: UserID) -> User | None:
        raise NotImplementedError
