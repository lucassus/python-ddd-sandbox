from dataclasses import dataclass

from app.shared.base_aggregate import BaseAggregate
from app.shared.message_bus import BaseEvent


@dataclass
class User(BaseAggregate):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: int

    email: str  # TODO: Create value object with validation
    password: str
