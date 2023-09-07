from dataclasses import dataclass

from app.infrastructure.message_bus import Event
from app.modules.shared_kernel.entities.user_id import UserID


@dataclass(frozen=True)
class UserAccountCreated(Event):
    user_id: UserID
