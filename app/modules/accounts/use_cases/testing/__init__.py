from typing import Optional

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.accounts.use_cases.testing.fake_repository import FakeRepository  # noqa
from app.modules.accounts.use_cases.testing.fake_unit_of_work import FakeUnitOfWork  # noqa


def build_user(
    email: Optional[EmailAddress] = None,
    password: Optional[Password] = None,
) -> User:
    if email is None:
        email = EmailAddress("test@email.com")

    if password is None:
        password = Password("password")

    return User(email=email, password=password)
