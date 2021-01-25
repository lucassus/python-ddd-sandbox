import abc

from todos.services.accounts.domain.entities import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, task: User) -> None:
        raise NotImplementedError
