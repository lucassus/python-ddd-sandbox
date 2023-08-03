from typing import Callable

from sqlalchemy.orm import Session

from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.infrastructure.adapters.project_repository import ProjectRepository


class UnitOfWork(AbstractUnitOfWork):
    project: ProjectRepository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory

    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.project = ProjectRepository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
