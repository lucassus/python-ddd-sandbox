from app.modules.projects.application.commands import CreateExampleProject
from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project
from app.modules.shared_kernel.events import UserAccountCreated
from app.shared.message_bus import EventHandler, MessageBus


class CreateUserExampleProjectHandler(EventHandler[UserAccountCreated]):
    def __init__(self, bus: MessageBus):
        self._bus = bus

    def __call__(self, event: UserAccountCreated) -> None:
        self._bus.execute(CreateExampleProject(event.user_id))


class SendProjectCreatedMessage(EventHandler[Project.Created]):
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, event: Project.Created):
        with self._uow as uow:
            project = uow.projects.get(event.project_id)
            uow.commit()

        print(f"Project {project.name} has been created")
