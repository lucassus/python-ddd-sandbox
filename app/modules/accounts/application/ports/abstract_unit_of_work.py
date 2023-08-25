import abc
from contextlib import AbstractContextManager
from typing import Self

from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.shared_kernel.message_bus import MessageBus


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    user: AbstractUserRepository

    def __init__(self, bus: MessageBus):
        self._bus = bus

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when the session has been committed before

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
