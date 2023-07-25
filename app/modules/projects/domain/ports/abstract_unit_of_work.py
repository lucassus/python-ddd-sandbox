import abc

from app.modules.projects.domain.ports import AbstractRepository
from app.shared.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork, metaclass=abc.ABCMeta):
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
