import pytest
from sqlalchemy.orm.session import Session

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.command.accounts.entrypoints.adapters.sqla_user_repository import SQLAUserRepository


class TestRepository:
    @pytest.fixture
    def repository(self, session: Session):
        return SQLAUserRepository(session=session)

    def test_exists_by_email_returns_false(self, repository: SQLAUserRepository):
        assert repository.exists_by_email(EmailAddress("test@email.com")) is False

    def test_exists_by_email_returns_true(self, session: Session, repository: SQLAUserRepository):
        repository.create(User(email=EmailAddress("test@email.com"), password=Password("password")))
        session.commit()

        assert repository.exists_by_email(EmailAddress("test@email.com")) is True

    def test_create(self, session: Session, repository: SQLAUserRepository):
        user = User(email=EmailAddress("test@email.com"), password=Password("password"))
        repository.create(user)
        session.commit()

        assert user.id is not None
