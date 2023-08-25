import abc

from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class AbstractUserRepository(metaclass=abc.ABCMeta):
    # Repositories are part of domain layer, therefore it is more appropriate
    # to use value object not just a string.
    @abc.abstractmethod
    def exists_by_email(self, email: EmailAddress) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id: UserID) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: EmailAddress) -> User | None:
        raise NotImplementedError
