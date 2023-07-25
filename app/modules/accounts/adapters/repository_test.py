import pytest
from sqlalchemy.orm.session import Session

from app.modules.accounts.adapters.repository import Repository
from app.modules.accounts.domain.entities import User


@pytest.fixture
def repository(session: Session):
    return Repository(session=session)


def test_repository_exists_by_email_returns_false(repository: Repository):
    assert repository.exists_by_email("test@email.com") is False


def test_repository_exists_by_email_returns_true(session: Session, repository: Repository):
    repository.create(User(email="test@email.com", password="password"))
    session.commit()

    assert repository.exists_by_email("test@email.com") is True
