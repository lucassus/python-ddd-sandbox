from typing import Optional

from app.command.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.accounts.entities.email_address import EmailAddress
from app.command.accounts.entities.errors import EmailAlreadyExistsException
from app.command.accounts.entities.password import Password
from app.command.accounts.entities.user import User
from app.shared_kernel.message_bus import BaseEvent, MessageBus
from app.shared_kernel.user_id import UserID


class NoopMessageBus(MessageBus):
    def dispatch(self, event: BaseEvent) -> None:
        pass


class RegisterUser:
    def __init__(
        self,
        *,
        uow: AbstractUnitOfWork,
        bus: Optional[MessageBus] = None,
    ):
        self._uow = uow
        self._bus = bus if bus is not None else NoopMessageBus()

    def __call__(self, *, email: EmailAddress, password: Password) -> UserID:
        with self._uow as uow:
            if uow.user.exists_by_email(email):
                raise EmailAlreadyExistsException(email)

            user = uow.user.create(User(email=email, password=password))
            uow.commit()

            self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))

            return user.id
