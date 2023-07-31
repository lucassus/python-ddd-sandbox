from typing import Callable

from sqlalchemy.orm import Session

from app.command.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.accounts.infrastructure.adapters.sqla_user_repository import SQLAUserRepository


class SQLAUnitOfWork(AbstractUnitOfWork):
    repository: SQLAUserRepository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory

    def __enter__(self) -> "SQLAUnitOfWork":
        self._session = self._session_factory()
        self.user = SQLAUserRepository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
