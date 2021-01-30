import abc

from app.services.projects.domain.ports import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    """
    Example usage:
        class ConcreteUnitOfWork(AbstractUnitOfWork):
            ...

        with ConcreteUnitOfWork() as uow:
            project = uow.repository.get(1)
            project.add_task(name="Buy a milk")
            uow.commit()
    """

    repository: AbstractRepository

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
