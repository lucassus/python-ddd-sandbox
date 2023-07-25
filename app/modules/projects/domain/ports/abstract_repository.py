import abc

from app.modules.projects.domain.entities import Project


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> Project:
        raise NotImplementedError
