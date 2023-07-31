from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.accounts.application.testing.factories import build_test_user
from app.command.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.command.accounts.entities.email_address import EmailAddress


def test_fake_repository():
    repository: AbstractUserRepository = FakeUserRepository()

    user = repository.create(build_test_user())
    assert user.id == 1

    loaded = repository.get(user.id)
    assert loaded is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
