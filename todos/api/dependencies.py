import functools

from fastapi import Depends
from sqlalchemy.orm import Session

from todos.domain.models.todo import Todo
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.service_layer import services


def get_session():
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_repository(session: Session = Depends(get_session)) -> AbstractRepository:
    return Repository(session=session)


class Service:
    def __init__(self, session: Session = Depends(get_session)):
        deps = dict(
            session=session,
            repository=Repository(session=session),
        )

        self._create_todo = functools.partial(services.create_todo, **deps)
        self._complete_todo = functools.partial(services.complete_todo, **deps)
        self._incomplete_todo = functools.partial(services.incomplete_todo, **deps)

    def create_todo(self, *, name: str) -> Todo:
        return self._create_todo(name=name)

    def complete_todo(self, id: str) -> Todo:
        return self._complete_todo(id=id)

    def incomplete_todo(self, id: str) -> Todo:
        return self._incomplete_todo(id=id)
