from dataclasses import dataclass

from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.password import Password
from app.shared_kernel.base_aggregate import BaseAggregate
from app.shared_kernel.message_bus import BaseEvent
from app.shared_kernel.user_id import UserID


@dataclass
class User(BaseAggregate[UserID]):
    @dataclass
    class AccountCreatedEvent(BaseEvent):
        user_id: UserID

    email: EmailAddress
    password: Password
