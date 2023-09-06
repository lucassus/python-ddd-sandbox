from app.infrastructure.db import AppSession, engine
from app.modules.accounts.domain.user import User
from app.modules.projects.domain.project import Project
from app.modules.shared_kernel.message_bus import MessageBus

bus = MessageBus()


def _session_factory():
    return AppSession(bind=engine)


@bus.listen(User.AccountCreated)
def create_example_project_handler(event: User.AccountCreated):
    from app.modules.projects.application.commands import CreateExampleProject

    bus.execute(CreateExampleProject(user_id=event.user_id))


@bus.listen(User.AccountCreated)
def send_welcome_email_handler(event: User.AccountCreated):
    from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork

    with UnitOfWork(session_factory=_session_factory, bus=bus) as uow:
        user = uow.users.get(event.user_id)

        if user is not None:
            print(f"Sending welcome email to {user.email}")


@bus.listen(Project.Created)
def handle_project_created_event(event: Project.Created):
    print(f"Project {event.project_id} has been created")
