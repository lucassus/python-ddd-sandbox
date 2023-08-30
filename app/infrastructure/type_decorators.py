import uuid
from typing import Any

from sqlalchemy import String, Uuid, types

from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class UserIDType(types.TypeDecorator[Any]):
    impl = Uuid()
    cache_ok = True

    def process_bind_param(self, value, dialect) -> uuid.UUID | None:
        if value is None:
            return None

        return uuid.UUID(str(value))

    def process_result_value(self, value, dialect) -> UserID | None:
        if value is None:
            return None

        return UserID(value)


class EmailType(types.TypeDecorator[Any]):
    impl = String(128)
    cache_ok = True

    def process_bind_param(self, value, dialect) -> str:
        return str(value)

    def process_result_value(self, value, dialect) -> EmailAddress:
        return EmailAddress(value)
