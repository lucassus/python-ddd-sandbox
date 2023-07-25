from typing import Any

from sqlalchemy import String, types

from app.modules.accounts.domain.email_address import EmailAddress


class EmailType(types.TypeDecorator[Any]):
    impl = String(255)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if isinstance(value, EmailAddress):
            return value.address

        return value

    def process_result_value(self, value, dialect):
        return EmailAddress(value)
