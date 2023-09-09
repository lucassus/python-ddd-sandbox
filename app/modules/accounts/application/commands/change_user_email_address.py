from dataclasses import dataclass

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException, UserNotFoundError
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.shared.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class ChangeUserEmailAddress(Command[None]):
    user_id: UserID
    new_email: EmailAddress


class ChangeUserEmailAddressHandler(CommandHandler[ChangeUserEmailAddress, None]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, command: ChangeUserEmailAddress) -> None:
        user_id, new_email = command.user_id, command.new_email

        with self._uow as uow:
            user = uow.users.get(user_id)

            if user is None:
                raise UserNotFoundError(user_id)

            if user.email == new_email:
                return

            if uow.users.exists_by_email(new_email):
                raise EmailAlreadyExistsException(new_email)

            user.email = new_email
            uow.commit()
