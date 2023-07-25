from dataclasses import dataclass

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.shared.base_aggregate import BaseAggregate
from app.shared.message_bus import BaseEvent


@dataclass
class User(BaseAggregate):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: int

    email: EmailAddress
    password: Password
