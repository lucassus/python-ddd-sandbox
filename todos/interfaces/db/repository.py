from typing import List, Optional

from sqlalchemy.orm.session import Session

from todos.domain.models import Task
from todos.interfaces.abstract_repository import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Optional[Task]:
        return self._session.query(Task).get(id)

    def list(self) -> List[Task]:
        return self._session.query(Task).all()

    def create(self, task: Task) -> None:
        self._session.add(task)
