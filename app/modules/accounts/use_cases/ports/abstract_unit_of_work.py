import abc

from app.modules.accounts.use_cases.ports import AbstractRepository
from app.shared_kernel.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    user: AbstractRepository
