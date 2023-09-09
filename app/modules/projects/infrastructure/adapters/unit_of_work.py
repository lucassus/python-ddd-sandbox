from typing import Callable

from sqlalchemy.orm import Session

from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.infrastructure.adapters.project_repository import ProjectRepository
from app.shared.message_bus import SupportsDispatchingEvents


class UnitOfWork(AbstractUnitOfWork):
    projects: ProjectRepository

    def __init__(self, session_factory: Callable[..., Session], bus: SupportsDispatchingEvents):
        super().__init__(bus)
        self._session_factory = session_factory

    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.projects = ProjectRepository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def _commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
