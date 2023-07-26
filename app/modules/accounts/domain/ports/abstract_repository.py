import abc

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.user import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def exists_by_email(self, email: EmailAddress) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id) -> User | None:
        raise NotImplementedError
