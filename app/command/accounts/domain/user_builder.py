from typing import Self

from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.password import Password
from app.command.accounts.domain.user import User


class UserBuilder:
    # Provide some sane defaults
    _email = EmailAddress("test@email.com")
    _password = Password("password")

    def with_email(self, email: str | EmailAddress) -> Self:
        self._email = EmailAddress(str(email))
        return self

    def build(self) -> User:
        return User(email=self._email, password=self._password)
