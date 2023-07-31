from typing import Any

from sqlalchemy import String, types

from app.command.accounts.domain.email_address import EmailAddress
from app.command.accounts.domain.password import Password


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
