from typing import List, Optional

from sqlalchemy.orm.session import Session

from todos.db.abstract_repository import AbstractRepository
from todos.domain.models.todo import Todo


class Repository(AbstractRepository):
    # TODO: How to correctly type class members?
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Optional[Todo]:
        return self._session.query(Todo).get(id)

    def list(self) -> List[Todo]:
        return self._session.query(Todo).all()

    # TODO: Change the signature to `add(self, todo: Todo) -> None`
    def create(self, name: str) -> Todo:
        todo = Todo(name=name)
        self._session.add(todo)

        return todo
