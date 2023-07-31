import abc

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.user import User
from app.shared_kernel.user_id import UserID


class AbstractUserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def exists_by_email(self, email: EmailAddress) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id: UserID) -> User | None:
        raise NotImplementedError
