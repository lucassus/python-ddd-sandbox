import abc

from app.modules.projects.entities.project import Project, ProjectID


class AbstractProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: ProjectID) -> Project:
        raise NotImplementedError
