from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.ports import AbstractUnitOfWork
from app.modules.accounts.domain.user import User
from app.shared_kernel.message_bus import MessageBus
from app.shared_kernel.user_id import UserID


class RegisterUser:
    def __init__(self, *, uow: AbstractUnitOfWork, bus: MessageBus):
        self._uow = uow
        self._bus = bus

    def __call__(self, *, email: EmailAddress, password: Password) -> UserID:
        with self._uow as uow:
            if uow.repository.exists_by_email(email):
                raise EmailAlreadyExistsException(email)

            user = User(email=email, password=password)
            uow.repository.create(user)
            uow.commit()

            self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))

            return user.id
