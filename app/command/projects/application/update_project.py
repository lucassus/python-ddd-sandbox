from app.command.projects.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.command.projects.entities.project import Project, ProjectID, ProjectName
from app.command.projects.entities.specifications import ActiveProjectSpecification


class UpdateProject:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow
        self._active = ActiveProjectSpecification()

    def _get_active_project(self, project_id: ProjectID) -> Project:
        return self._active.satisfied_from(self._uow.project, by=project_id)

    def __call__(self, project_id: ProjectID, name: ProjectName):
        with self._uow as uow:
            project = self._get_active_project(project_id)
            project.name = name
            uow.commit()
