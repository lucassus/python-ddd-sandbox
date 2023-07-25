from dataclasses import dataclass

from app.shared.base_aggregate import BaseAggregate
from app.shared.email_address import EmailAddress
from app.shared.message_bus import BaseEvent


@dataclass
class User(BaseAggregate):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: int

    email: EmailAddress
    password: str
