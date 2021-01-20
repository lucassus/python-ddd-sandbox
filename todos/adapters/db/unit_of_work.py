from typing import Callable

from sqlalchemy.orm import Session

from todos.adapters.db.repository import Repository
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    repository: Repository

    def __init__(self, session_factory: Callable[..., Session]):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.repository = Repository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()
        self.rollback()  # It does nothing when the session has been committed before

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
