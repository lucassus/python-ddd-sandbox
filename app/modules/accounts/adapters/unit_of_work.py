from typing import Callable

from sqlalchemy.orm import Session

from app.modules.accounts.adapters.repository import Repository
from app.modules.accounts.domain.ports import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    repository: Repository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory
        self._repository_factory = lambda: Repository(session=self._session)

    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.repository = self._repository_factory()

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
