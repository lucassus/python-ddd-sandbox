import abc

from app.modules.accounts.domain.entities import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abc.abstractmethod
    def create(self, user: User):
        raise NotImplementedError
