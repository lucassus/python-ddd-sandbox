from app.modules.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.projects.domain.project import ProjectID, ProjectName


class UpdateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, project_id: ProjectID, name: ProjectName):
        with self._uow as uow:
            project = uow.projects.get(project_id)
            project.name = name
            uow.commit()
