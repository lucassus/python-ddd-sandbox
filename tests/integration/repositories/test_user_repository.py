import pytest
from sqlalchemy.orm.session import Session

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.command.accounts.infrastructure.adapters.user_repository import UserRepository
from app.shared_kernel.user_id import UserID


class TestUserRepository:
    @pytest.fixture
    def repository(self, session: Session):
        return UserRepository(session=session)

    def test_exists_by_email_returns_false(self, repository: UserRepository):
        assert repository.exists_by_email(EmailAddress("test@email.com")) is False

    def test_exists_by_email_returns_true(self, create_user, repository: UserRepository):
        create_user(email=EmailAddress("test@email.com"))
        assert repository.exists_by_email(EmailAddress("test@email.com")) is True

    def test_create(self, session: Session, repository: UserRepository):
        user = User(email=EmailAddress("test@email.com"), password=Password("password"))
        repository.create(user)
        session.commit()

        assert user.id is not None

    def test_get(self, create_user, repository: UserRepository):
        user_id = create_user().id
        assert repository.get(user_id) is not None

    def test_get_returns_none_when_not_found(self, repository: UserRepository):
        assert repository.get(UserID(1)) is None