from dataclasses import dataclass

from app.common.base_entity import BaseEntity
from app.common.message_bus import BaseEvent


@dataclass
class User(BaseEntity):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: int

    email: str
    password: str
