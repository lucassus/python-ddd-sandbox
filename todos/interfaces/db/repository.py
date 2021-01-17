from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from todos.domain.models import Project
from todos.interfaces.abstract_repository import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def get(self) -> Optional[Project]:
        try:
            return self._session.query(Project).one()
        except NoResultFound:
            return None

    def list(self) -> List[Project]:
        return self._session.query(Project).all()

    def create(self, task: Project) -> None:
        self._session.add(task)
