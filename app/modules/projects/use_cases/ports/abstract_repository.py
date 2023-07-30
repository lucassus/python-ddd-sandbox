import abc

from app.modules.projects.domain.project import Project, ProjectID


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: ProjectID) -> Project:
        raise NotImplementedError
