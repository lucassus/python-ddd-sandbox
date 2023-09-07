from app.infrastructure.db import AppSession, engine
from app.infrastructure.message_bus import MessageBus
from app.modules.shared_kernel.events import UserAccountCreated
from app.modules.projects.domain.project import Project


def register_event_handlers(bus: MessageBus) -> None:
    # TODO: Move to projects module
    @bus.listen(UserAccountCreated)
    def create_example_project_handler(event: UserAccountCreated):
        from app.modules.projects.application.commands import CreateExampleProject

        bus.execute(CreateExampleProject(user_id=event.user_id))

    # TODO: Move to accounts module
    @bus.listen(UserAccountCreated)
    def send_welcome_email_handler(event: UserAccountCreated):
        from app.modules.accounts.infrastructure.adapters.unit_of_work import UnitOfWork

        with UnitOfWork(session_factory=lambda: AppSession(bind=engine), bus=bus) as uow:
            user = uow.users.get(event.user_id)

            if user is not None:
                print(f"Sending welcome email to {user.email}")

    # TODO: Move to projects module
    @bus.listen(Project.Created)
    def handle_project_created_event(event: Project.Created):
        print(f"Project {event.project_id} has been created")
