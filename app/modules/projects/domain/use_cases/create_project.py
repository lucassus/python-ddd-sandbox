from app.modules.projects.domain.entities import Project, ProjectID
from app.modules.projects.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


class CreateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, user_id: UserID, name: str) -> ProjectID:
        with self._uow as uow:
            project = Project(name=name)
            project.user_id = user_id

            project = uow.repository.create(project)
            uow.commit()

            return project.id
