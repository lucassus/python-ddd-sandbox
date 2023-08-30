import abc

from app.modules.accounts.domain.password import Password


class AbstractPasswordHasher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def hash(self, password: Password) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, password: Password, hashed_password: str) -> bool:
        raise NotImplementedError
