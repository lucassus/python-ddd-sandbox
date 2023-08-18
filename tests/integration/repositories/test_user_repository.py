import pytest
from sqlalchemy.orm.session import Session

from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.accounts.infrastructure.adapters.user_repository import UserRepository
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class TestUserRepository:
    @pytest.fixture()
    def repository(self, session: Session):
        return UserRepository(session=session)

    def test_exists_by_email_returns_false(self, repository: UserRepository):
        assert repository.exists_by_email(EmailAddress("test@email.com")) is False

    def test_exists_by_email_returns_true(self, create_user, repository: UserRepository):
        create_user(email=EmailAddress("test@email.com"))
        assert repository.exists_by_email(EmailAddress("test@email.com")) is True

    def test_create(self, session: Session, repository: UserRepository):
        user = UserBuilder().build()
        repository.create(user)
        session.commit()

        assert user.id is not None

    def test_get(self, create_user, repository: UserRepository):
        user_id = create_user().id
        assert repository.get(user_id) is not None

    def test_get_returns_none_when_not_found(self, repository: UserRepository):
        assert repository.get(UserID(1)) is None

    def test_get_by_email(self, create_user, repository: UserRepository):
        user = create_user()
        assert repository.get_by_email(user.email) is not None

    def test_get_by_email_returns_none_when_not_found(self, repository: UserRepository):
        assert repository.get_by_email(EmailAddress("non-existing@email.com")) is None
