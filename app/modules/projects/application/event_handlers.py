from app.infrastructure.message_bus import MessageBus
from app.modules.projects.domain.project import Project
from app.modules.shared_kernel.events import UserAccountCreated
from app.modules.projects.application.commands import CreateExampleProject


# TODO: This is application but it takes a dependency from the infra, fix it


def register_event_handlers(bus: MessageBus) -> None:
    @bus.listen(UserAccountCreated)
    def create_example_project_handler(event: UserAccountCreated):
        bus.execute(CreateExampleProject(event.user_id))

    @bus.listen(Project.Created)
    def handle_project_created_event(event: Project.Created):
        print(f"Project {event.project_id} has been created")
