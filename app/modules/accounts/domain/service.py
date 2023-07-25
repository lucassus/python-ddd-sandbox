from app.modules.accounts.domain.entities import User
from app.modules.accounts.domain.ports import AbstractUnitOfWork
from app.shared.message_bus import MessageBus


class Service:
    def __init__(self, *, uow: AbstractUnitOfWork, bus: MessageBus):
        self._uow = uow
        self._bus = bus

    def register_user(self, *, email: str, password: str) -> int:
        with self._uow as uow:
            user = User(email=email, password=password)
            uow.repository.create(user)
            uow.commit()

            self._bus.dispatch(User.AccountCreatedEvent(user_id=user.id))

            return user.id
