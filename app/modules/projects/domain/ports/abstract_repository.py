import abc

from app.modules.projects.domain.entities import Project


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def list(self) -> list[Project]:
        raise NotImplementedError
