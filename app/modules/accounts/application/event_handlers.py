from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import EventHandler


class SendWelcomeEmail(EventHandler[UserAccountCreated]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, event: UserAccountCreated):
        with self._uow as uow:
            user = uow.users.get(event.user_id)

            if user is not None:
                print(f"Sending welcome email to {user.email}")
