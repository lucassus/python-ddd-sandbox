from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.user_builder import UserBuilder


def test_fake_repository():
    repository: AbstractUserRepository = FakeUserRepository()

    user = repository.create(UserBuilder().build())
    assert user.id == 1

    loaded = repository.get(user.id)
    assert loaded is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
