from typing import Optional

from sqlalchemy.orm import Session

from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal


# TODO: Inject the session and start the nested transaction
class UnitOfWork(AbstractUnitOfWork):
    _session: Optional[Session]

    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    @property
    def repository(self) -> Repository:
        return Repository(session=self._session)

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
