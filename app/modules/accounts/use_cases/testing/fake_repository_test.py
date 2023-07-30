from app.modules.accounts.domain import EmailAddress
from app.modules.accounts.use_cases.ports import AbstractRepository
from app.modules.accounts.use_cases.testing import FakeRepository, build_user


def test_fake_repository():
    repository: AbstractRepository = FakeRepository()

    user = repository.create(build_user())
    assert user.id == 1

    loaded = repository.get(user.id)
    assert loaded is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
