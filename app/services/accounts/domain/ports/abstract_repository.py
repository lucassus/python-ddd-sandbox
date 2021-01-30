import abc

from app.services.accounts.domain.entities import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> None:
        raise NotImplementedError
