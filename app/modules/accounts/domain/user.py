from dataclasses import dataclass
from typing import NewType

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.shared.base_aggregate import BaseAggregate
from app.shared.message_bus import BaseEvent

UserID = NewType("UserID", int)


@dataclass
class User(BaseAggregate[UserID]):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: UserID

    email: EmailAddress
    password: Password
