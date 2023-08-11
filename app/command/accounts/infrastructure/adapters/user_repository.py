from sqlalchemy import select
from sqlalchemy.orm.session import Session

from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.user import User
from app.infrastructure.tables import users_table


class UserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self._session = session

    def exists_by_email(self, email: EmailAddress) -> bool:
        query = select(users_table.c.id).where(users_table.c.email == email)
        user_id = self._session.execute(query).scalar_one_or_none()
        return user_id is not None

    def create(self, user: User) -> User:
        self._session.add(user)
        return user

    def get(self, user_id) -> User | None:
        return self._session.get(User, user_id)
