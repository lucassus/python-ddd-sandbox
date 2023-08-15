from app.infrastructure.db import AppSession
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.message_bus import MessageBus

bus = MessageBus()


@bus.listen(User.AccountCreatedEvent)
def create_example_project_handler(event: User.AccountCreatedEvent):
    from app.modules.projects.application.create_example_project import CreateExampleProject
    from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork

    uow = UnitOfWork(session_factory=AppSession)
    create_example_project = CreateExampleProject(uow=uow)

    create_example_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email_handler(event: User.AccountCreatedEvent):
    from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=AppSession) as uow:
        user = uow.user.get(event.user_id)

        if user is not None:
            print(f"Sending welcome email to {user.email}")