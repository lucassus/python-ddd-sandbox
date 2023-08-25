from app.infrastructure.db import AppSession, engine
from app.modules.accounts.domain.user import User
from app.modules.projects.domain.project import Project
from app.modules.shared_kernel.message_bus import MessageBus

bus = MessageBus()


def _session_factory():
    return AppSession(bind=engine)


@bus.listen(User.AccountCreatedEvent)
def create_example_project_handler(event: User.AccountCreatedEvent):
    from app.modules.projects.application.create_example_project import CreateExampleProject
    from app.modules.projects.infrastructure.adapters.unit_of_work import UnitOfWork

    uow = UnitOfWork(session_factory=_session_factory)
    create_example_project = CreateExampleProject(uow=uow, bus=bus)

    create_example_project(user_id=event.user_id)


@bus.listen(User.AccountCreatedEvent)
def send_welcome_email_handler(event: User.AccountCreatedEvent):
    from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=_session_factory, bus=bus) as uow:
        user = uow.users.get(event.user_id)

        if user is not None:
            print(f"Sending welcome email to {user.email}")


@bus.listen(Project.CreatedEvent)
def handle_project_created_event(event: Project.CreatedEvent):
    print(f"Project {event.project_id} has been created")
