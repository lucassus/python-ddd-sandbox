from sqlalchemy.orm.session import Session

from todos.services.accounts.domain.entities import User
from todos.services.accounts.domain.ports import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: User) -> None:
        self._session.add(user)
