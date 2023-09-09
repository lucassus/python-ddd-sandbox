from dataclasses import dataclass

from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import Event


@dataclass(frozen=True)
class UserAccountCreated(Event):
    user_id: UserID
