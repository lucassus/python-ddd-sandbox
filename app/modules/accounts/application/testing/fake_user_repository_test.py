from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.email_address import EmailAddress


def test_fake_repository():
    repository: AbstractUserRepository = FakeUserRepository()

    user = repository.create(UserBuilder().build())
    assert user.id == 1

    loaded = repository.get(user.id)
    assert loaded is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
