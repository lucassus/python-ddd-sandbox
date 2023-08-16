import abc

from app.modules.projects.application.ports.abstract_project_repository import AbstractProjectRepository
from app.modules.shared_kernel.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    """
    Example usage:
        class ConcreteUnitOfWork(AbstractUnitOfWork):
            ...

        with ConcreteUnitOfWork() as uow:
            project = uow.repository.get(1)
            project.add_task(name="Buy a milk")
            uow.commit()
    """

    project: AbstractProjectRepository
