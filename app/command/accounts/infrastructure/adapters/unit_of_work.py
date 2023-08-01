from typing import Callable

from sqlalchemy.orm import Session

from app.command.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.accounts.infrastructure.adapters.user_repository import UserRepository


class UnitOfWork(AbstractUnitOfWork):
    repository: UserRepository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory

    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.user = UserRepository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
