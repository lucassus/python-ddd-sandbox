import abc

from app.command.projects.entities.project import Project, ProjectID


class AbstractProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get_active(self, id: ProjectID) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get_archived(self, id: ProjectID) -> Project:
        raise NotImplementedError
