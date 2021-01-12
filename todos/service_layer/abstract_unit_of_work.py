import abc

from todos.db.abstract_repository import AbstractRepository


# TODO: Should I use this pattern for reading
class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when commit has been called before

    @property
    @abc.abstractmethod
    def todos(self) -> AbstractRepository:
        pass

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
