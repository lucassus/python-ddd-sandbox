from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.ports import AbstractRepository
from app.modules.accounts.domain.user import User


def test_fake_repository(repository: AbstractRepository):
    user = User(email=EmailAddress("test@email.com"), password=Password("password"))
    repository.create(user)
    assert user.id == 1

    user = repository.get(user.id)
    assert user is not None

    assert repository.exists_by_email(user.email) is True
    assert repository.exists_by_email(EmailAddress("non-existing@email.com")) is False
