from app.common.message_bus import MessageBus
from app.infrastructure.session import session_factory
from app.services.accounts.domain.entities import User

bus = MessageBus()


# TODO: Perhaps event handlers should be placed somewhere else


@bus.listen(User.AccountCreatedEvent)
def create_first_project(event: User.AccountCreatedEvent):
    from app.services.project_management.adapters.unit_of_work import UnitOfWork
    from app.services.project_management.domain.service import Service

    uow = UnitOfWork(session_factory=session_factory)
    service = Service(uow=uow)

    return service.create_first_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email(event: User.AccountCreatedEvent):
    from app.services.accounts.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=session_factory) as uow:
        user = uow.repository.get(event.user_id)
        print(f"Sending welcome email to {user}")
