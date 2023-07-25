from app.infrastructure.db import AppSession
from app.modules.accounts.domain.entities import User
from app.shared.message_bus import MessageBus

bus = MessageBus()


# TODO: Perhaps event handlers should be placed somewhere else


@bus.listen(User.AccountCreatedEvent)
def create_first_project(event: User.AccountCreatedEvent):
    from app.modules.projects.adapters.unit_of_work import UnitOfWork
    from app.modules.projects.domain.service import Service

    uow = UnitOfWork(session_factory=AppSession)
    service = Service(uow=uow)

    return service.create_first_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email(event: User.AccountCreatedEvent):
    from app.modules.accounts.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=AppSession) as uow:
        user = uow.repository.get(event.user_id)
        print(f"Sending welcome email to {user}")
