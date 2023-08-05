from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import ProjectID, ProjectName


class UpdateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, project_id: ProjectID, name: ProjectName):
        with self._uow as uow:
            project = uow.project.get(project_id)
            project.name = name
            uow.commit()
