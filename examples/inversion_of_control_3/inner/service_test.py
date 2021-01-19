from examples.inversion_of_control_3.inner.abstract_repository import AbstractRepository
from examples.inversion_of_control_3.inner.service import Service
from examples.user import User


class FakeRepository(AbstractRepository):
    def get_user(self) -> User:
        return User(name="Faker")


def test_service():
    service = Service(repository=FakeRepository())
    assert service() == "Hello, Faker!"
