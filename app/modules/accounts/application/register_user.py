from typing import Annotated

from pydantic import Field
from pydantic.types import UuidVersion

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password_field import PasswordField
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus
from app.shared.base_schema import BaseSchema
from app.shared.email_address_field import EmailAddressField


class RegisterUser:
    class Command(BaseSchema):
        id: Annotated[UserID, UuidVersion(4), Field(default_factory=lambda: UserID.generate())]
        email: EmailAddressField
        password: PasswordField

    def __init__(self, *, uow: AbstractUnitOfWork, bus: MessageBus):
        self._uow = uow
        self._bus = bus

    def __call__(self, command: Command):
        id, email, password = command.id, command.email, command.password

        with self._uow as uow:
            if uow.user.exists_by_email(email):
                raise EmailAlreadyExistsException(email)

            user = uow.user.create(User(id=id, email=email, password=password))
            uow.commit()

        self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))
