from dataclasses import dataclass, field

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.shared_kernel.aggregate_root import AggregateRoot
from app.shared_kernel.message_bus import BaseEvent
from app.shared_kernel.user_id import UserID


@dataclass
class User(AggregateRoot):
    @dataclass(frozen=True)
    class AccountCreatedEvent(BaseEvent):
        user_id: UserID

    id: UserID = field(init=False)
    email: EmailAddress
    password: Password
