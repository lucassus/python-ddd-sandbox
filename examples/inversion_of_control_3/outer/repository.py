from examples.inversion_of_control_3.inner.ports import AbstractRepository
from examples.user import User


class Repository(AbstractRepository):
    def get_user(self) -> User:
        return User(name="Luke")
