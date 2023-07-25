import abc

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.entities import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def exists_by_email(self, email: EmailAddress) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User):
        raise NotImplementedError
