import pytest
from sqlalchemy.orm import Session

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.command.accounts.infrastructure.adapters.user_repository import UserRepository


@pytest.fixture
def create_user(session: Session):
    repository = UserRepository(session=session)

    def _create_user(email: EmailAddress | None = None):
        user = User(
            email=email or EmailAddress("test@email.com"),
            password=Password("password"),
        )

        repository.create(user)
        session.commit()

        return user

    return _create_user
