from app.infrastructure.db import AppSession, engine
from app.infrastructure.message_bus import MessageBus
from app.modules.shared_kernel.events import UserAccountCreated


def register_event_handlers(bus: MessageBus) -> None:
    @bus.listen(UserAccountCreated)
    def send_welcome_email_handler(event: UserAccountCreated):
        # TODO: This is wrong, figure how to inject unit of work here...
        from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork

        with UnitOfWork(session_factory=lambda: AppSession(bind=engine), bus=bus) as uow:
            user = uow.users.get(event.user_id)

            if user is not None:
                print(f"Sending welcome email to {user.email}")
