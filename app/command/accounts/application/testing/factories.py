from typing import Optional

from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User


def build_test_user(
    email: Optional[EmailAddress] = None,
    password: Optional[Password] = None,
) -> User:
    if email is None:
        email = EmailAddress("test@email.com")

    if password is None:
        password = Password("password")

    return User(email=email, password=password)
