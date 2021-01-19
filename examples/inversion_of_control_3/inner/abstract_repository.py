import abc

from examples.user import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_user(self) -> User:
        raise NotImplementedError
