from app.command.accounts.entities.user import User
from app.infrastructure.db import AppSession
from app.shared_kernel.message_bus import MessageBus

# TODO: Maybe move it to infrastructure?
bus = MessageBus()


@bus.listen(User.AccountCreatedEvent)
def create_example_project_handler(event: User.AccountCreatedEvent):
    from app.command.projects.application.create_example_project import CreateExampleProject
    from app.command.projects.entrypoints.adapters.sqla_unit_of_work import SQLAUnitOfWork

    uow = SQLAUnitOfWork(session_factory=AppSession)
    create_example_project = CreateExampleProject(uow=uow)

    create_example_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email_handler(event: User.AccountCreatedEvent):
    from app.command.accounts.entrypoints.adapters.sqla_unit_of_work import SQLAUnitOfWork

    with SQLAUnitOfWork(session_factory=AppSession) as uow:
        user = uow.user.get(event.user_id)
        print(f"Sending welcome email to {user.email}")
