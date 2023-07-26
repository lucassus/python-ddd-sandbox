import abc

from app.modules.accounts.domain.ports import AbstractRepository
from app.shared_kernel.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork, metaclass=abc.ABCMeta):
    repository: AbstractRepository
