from dataclasses import dataclass

from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import Command, CommandHandler


@dataclass(frozen=True)
class RegisterUser(Command):
    user_id: UserID
    email: EmailAddress
    password: Password


class RegisterUserHandler(CommandHandler[RegisterUser]):
    def __init__(
        self,
        *,
        uow: AbstractUnitOfWork,
        password_hasher: AbstractPasswordHasher,
    ):
        self._uow = uow
        self._password_hasher = password_hasher

    def __call__(self, command: RegisterUser):
        user_id, email, password = command.user_id, command.email, command.password

        with self._uow as uow:
            if uow.users.exists_by_email(email):
                raise EmailAlreadyExistsException(email)

            uow.users.create(
                User(
                    id=user_id,
                    email=email,
                    hashed_password=self._password_hasher.hash(password),
                )
            )

            uow.commit()
