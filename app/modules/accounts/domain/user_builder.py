from typing import Self

from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class UserBuilder:
    # Provide some sane defaults
    _email = EmailAddress("test@email.com")
    _password = Password("password")

    def __init__(self):
        self._id = UserID.generate()

    def with_id(self, id: UserID) -> Self:
        self._id = id
        return self

    def with_email(self, email: str | EmailAddress) -> Self:
        self._email = EmailAddress(str(email))
        return self

    def with_password(self, password: str | Password) -> Self:
        self._password = Password(str(password))
        return self

    def build(self) -> User:
        return User(
            id=self._id,
            email=self._email,
            password=self._password,
        )
