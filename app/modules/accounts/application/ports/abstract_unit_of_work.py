import abc
from contextlib import AbstractContextManager
from typing import Self

from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.shared_kernel.message_bus import SupportsDispatch


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    users: AbstractUserRepository

    def __init__(self, bus: SupportsDispatch):
        self._bus = bus

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when the session has been committed before

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    def commit(self):
        self._commit()

        for user in self.users.seen:
            for event in user.events:
                self._bus.dispatch(event)

            user.events.clear()

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
