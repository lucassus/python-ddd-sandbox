from sqlalchemy.orm.session import Session

from app.modules.accounts.domain.entities import User
from app.modules.accounts.domain.ports import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: User) -> None:
        self._session.add(user)

    def get(self, id: int) -> User:
        return self._session.query(User).get(id)
