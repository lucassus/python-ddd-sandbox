import abc

from app.command.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.command.shared_kernel.base_unit_of_work import BaseUnitOfWork


class AbstractUnitOfWork(BaseUnitOfWork["AbstractUnitOfWork"], metaclass=abc.ABCMeta):
    user: AbstractUserRepository
