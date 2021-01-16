import abc

from todos.interfaces.abstract_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when commit has been called before

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
