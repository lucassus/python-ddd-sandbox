from sqlalchemy import select
from sqlalchemy.orm.session import Session

from app.modules.accounts.domain.entities import User
from app.modules.accounts.domain.ports import AbstractRepository


class Repository(AbstractRepository):
    def __init__(self, session: Session):
        self._session = session

    def exists_by_email(self, email: str) -> bool:
        query = select(User.id).where(User.email == email)
        user_id = self._session.execute(query).scalar_one_or_none()
        return user_id is not None

    # Or a bit more efficient with inoperative style
    # def exists_by_email(self, email: str) -> bool:
    #     connection = self._session.connection()
    #     query = select(users_table.c.id).where(users_table.c.email == email)
    #     result = connection.execute(query).scalar_one_or_none()
    #
    #     return result is not None

    def create(self, user: User) -> None:
        self._session.add(user)
