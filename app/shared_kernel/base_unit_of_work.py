import abc
from contextlib import AbstractContextManager


class BaseUnitOfWork(AbstractContextManager["BaseUnitOfWork"]):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when the session has been committed before

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
