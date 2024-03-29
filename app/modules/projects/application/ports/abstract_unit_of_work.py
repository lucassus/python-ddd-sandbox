import abc
from contextlib import AbstractContextManager
from typing import Self

from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.shared.message_bus import SupportsDispatchingEvents


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    projects: AbstractProjectRepository

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
        for project in self.projects.seen:
            for event in project.events:
                self._bus.dispatch(event)

            project.clear_events()

    def commit(self):
        self._commit()
        self._publish_events()

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
