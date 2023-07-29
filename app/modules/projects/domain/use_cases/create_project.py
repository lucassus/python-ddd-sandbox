from app.modules.projects.domain.entities import Project, ProjectID
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


class CreateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, user_id: UserID, project_name: str) -> ProjectID:
        with self._uow as uow:
            new_project = Project(name=project_name)
            new_project.user_id = user_id

            new_project = uow.project.create(new_project)
            uow.commit()

            return new_project.id
