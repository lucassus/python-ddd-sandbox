import abc
from contextlib import AbstractContextManager
from typing import Self

from app.modules.accounts.application.ports.tracking_user_repository import TrackingUserRepository
from app.modules.shared_kernel.message_bus import SupportsDispatchingEvents


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    users: TrackingUserRepository

    def __init__(self, bus: SupportsDispatchingEvents):
        self._bus = bus

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when the session has been committed before

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    def _publish_events(self):
        for user in self.users.seen:
            for event in user.events:
                self._bus.dispatch(event)

            user.clear_events()

    def commit(self):
        self._commit()
        self._publish_events()

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
