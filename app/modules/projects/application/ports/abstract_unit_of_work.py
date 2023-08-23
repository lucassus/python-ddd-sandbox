import abc
from contextlib import AbstractContextManager

from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository


class AbstractUnitOfWork(AbstractContextManager["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    """
    Example usage:
        class ConcreteUnitOfWork(AbstractUnitOfWork):
            ...

        with ConcreteUnitOfWork() as uow:
            project = uow.project.get(1)
            project.add_task(name="Buy a milk")
            uow.commit()
    """

    project: AbstractProjectRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()  # It does nothing when the session has been committed before

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
