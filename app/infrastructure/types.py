from typing import Any

from sqlalchemy import String, types

from app.shared.email_address import EmailAddress


class EmailType(types.TypeDecorator[Any]):
    impl = String(255)

    def process_bind_param(self, value, dialect):
        if isinstance(value, EmailAddress):
            return value.address

        return value

    def process_result_value(self, value, dialect):
        return EmailAddress(value)
