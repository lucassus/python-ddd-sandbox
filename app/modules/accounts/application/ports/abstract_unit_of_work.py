import abc
from contextlib import AbstractContextManager

from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    user: AbstractUserRepository

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
