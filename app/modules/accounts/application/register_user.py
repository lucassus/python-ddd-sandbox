from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus


class RegisterUser:
    def __init__(self, *, uow: AbstractUnitOfWork, bus: MessageBus):
        self._uow = uow
        self._bus = bus

    def __call__(self, user_id: UserID, *, email: EmailAddress, password: Password):
        with self._uow as uow:
            if uow.user.exists_by_email(email):
                raise EmailAlreadyExistsException(email)

            user = uow.user.create(User(id=user_id, email=email, password=password))
            uow.commit()

        self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))
