from dataclasses import dataclass, field

from app.common.message_bus import BaseEvent


@dataclass
class User:
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: int

    id: int = field(init=False)
    email: str
    password: str
