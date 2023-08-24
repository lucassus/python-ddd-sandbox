from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project, ProjectID, ProjectName
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.message_bus import MessageBus


class CreateProject:
    def __init__(
        self,
        *,
        uow: AbstractUnitOfWork,
        bus: MessageBus,
    ):
        self._uow = uow
        self._bus = bus

    def __call__(self, user_id: UserID, name: ProjectName) -> ProjectID:
        new_project = Project(user_id=user_id, name=name)

        with self._uow as uow:
            new_project = uow.project.create(new_project)
            uow.commit()

        self._bus.dispatch(Project.CreatedEvent(project_id=new_project.id))

        return new_project.id
