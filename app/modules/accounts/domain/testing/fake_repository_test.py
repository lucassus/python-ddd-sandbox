from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.testing import build_user


def test_fake_repository(repository: AbstractRepository):
    user = build_user()
    repository.create(user)
    assert user.id == 1

    user = repository.get(user.id)
    assert user is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
