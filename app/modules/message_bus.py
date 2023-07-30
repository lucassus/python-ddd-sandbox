from app.infrastructure.db import AppSession
from app.modules.accounts.domain.user import User
from app.shared_kernel.message_bus import MessageBus

bus = MessageBus()


# TODO: Perhaps event handlers should be placed somewhere else
# TODO: Figure out how to test it


@bus.listen(User.AccountCreatedEvent)
def create_example_project_handler(event: User.AccountCreatedEvent):
    from app.modules.projects.adapters.unit_of_work import UnitOfWork
    from app.modules.projects.domain.use_cases.create_example_project import CreateExampleProject

    uow = UnitOfWork(session_factory=AppSession)

    create_example_project = CreateExampleProject(uow=uow)
    create_example_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email_handler(event: User.AccountCreatedEvent):
    from app.modules.accounts.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=AppSession) as uow:
        user = uow.user.get(event.user_id)
        print(f"Sending welcome email to {user}")
