from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.factories import build_example_project
from app.modules.projects.domain.project import Project, ProjectID
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus


class CreateExampleProject:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        bus: MessageBus,
    ):
        self.uow = uow
        self.bus = bus

    def __call__(self, user_id: UserID) -> ProjectID:
        new_project = build_example_project(user_id)

        with self.uow:
            self.uow.project.create(new_project)
            self.uow.commit()

        self.bus.dispatch(Project.CreatedEvent(project_id=new_project.id))

        return new_project.id
