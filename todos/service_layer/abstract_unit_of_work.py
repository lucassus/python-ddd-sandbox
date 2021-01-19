import abc

from todos.service_layer.abstract_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
