from fastapi import Depends
from sqlalchemy.orm import Session

from todos.domain.models import Task
from todos.interfaces.abstract_repository import AbstractRepository
from todos.interfaces.db.repository import Repository
from todos.interfaces.db.session import SessionLocal
from todos.service_layer import services
from todos.service_layer.unit_of_work import UnitOfWork


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


class CreateTaskHandler:
    def __init__(self):
        self._uof = UnitOfWork()

    def __call__(self, name: str) -> Task:
        return services.create_task(name, uof=self._uof)


class CompleteTaskHandler:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def __call__(self, task: Task) -> Task:
        return services.complete_task(task, session=self._session)


class IncompleteTaskHandler:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def __call__(self, task: Task) -> Task:
        return services.incomplete_task(task, session=self._session)
