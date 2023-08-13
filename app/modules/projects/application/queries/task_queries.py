import abc

from app.modules.projects.domain.project import ProjectID
from app.modules.projects.domain.task import TaskNumber

# TODO: Move schemas here


class AbstractFetchTasksQuery(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, *, project_id: ProjectID):
        raise NotImplementedError()


class AbstractFindTaskQuery(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, *, project_id: ProjectID, number: TaskNumber):
        raise NotImplementedError()
