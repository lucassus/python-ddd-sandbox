from typing import Optional

from sqlalchemy.orm import Session

from todos.db.repository import Repository
from todos.db.session import SessionLocal
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork


# TODO: http://io.made.com/blog/2017-09-08-repository-and-unit-of-work-pattern-in-python.html
class UnitOfWork(AbstractUnitOfWork):
    _session: Optional[Session]

    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

        # TODO: Find a better idea for cheking Optional
        assert self._session
        self._session.close()

    @property
    def todos(self) -> Repository:
        assert self._session
        return Repository(session=self._session)

    def commit(self):
        assert self._session
        self._session.commit()

    def rollback(self):
        assert self._session
        self._session.rollback()
