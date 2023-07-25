import abc

from app.modules.accounts.domain.ports import AbstractRepository
from app.shared.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork, metaclass=abc.ABCMeta):
    repository: AbstractRepository
