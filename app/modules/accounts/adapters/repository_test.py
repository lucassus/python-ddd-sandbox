import pytest
from sqlalchemy.orm.session import Session

from app.modules.accounts.adapters.repository import Repository
from app.modules.accounts.domain.entities import User


class TestRepository:
    @pytest.fixture
    def repository(self, session: Session):
        return Repository(session=session)

    def test_exists_by_email_returns_false(self, repository: Repository):
        assert repository.exists_by_email("test@email.com") is False

    def test_exists_by_email_returns_true(self, session: Session, repository: Repository):
        repository.create(User(email="test@email.com", password="password"))
        session.commit()

        assert repository.exists_by_email("test@email.com") is True

    def test_create(self, session: Session, repository: Repository):
        user = User(email="test@email.com", password="password")
        repository.create(user)
        session.commit()

        assert user.id is not None
