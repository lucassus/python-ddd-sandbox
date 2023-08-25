from typing import Any

from sqlalchemy import String, types, Uuid

from app.modules.accounts.domain.password import Password
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class UserIDType(types.TypeDecorator[Any]):
    impl = Uuid()
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, UserID):
            return value

        return value

    def process_result_value(self, value, dialect):
        return UserID(str(value))


class EmailType(types.TypeDecorator[Any]):
    impl = String(128)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, EmailAddress):
            return value.address

        return value

    def process_result_value(self, value, dialect):
        return EmailAddress(value)


class PasswordType(types.TypeDecorator[Any]):
    impl = String(64)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, Password):
            return value.value

        return value

    def process_result_value(self, value, dialect):
        return Password(value)
