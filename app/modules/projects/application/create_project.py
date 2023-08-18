from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import Project, ProjectID, ProjectName
from app.modules.shared_kernel.entities.user_id import UserID


class CreateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, user_id: UserID, name: ProjectName) -> ProjectID:
        new_project = Project(user_id=user_id, name=name)

        with self._uow as uow:
            new_project = uow.project.create(new_project)
            uow.commit()

            return new_project.id
