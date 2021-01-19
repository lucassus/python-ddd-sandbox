from examples.inversion_of_control_3.inner.abstract_repository import AbstractRepository
from examples.inversion_of_control_3.inner.service import Service
from examples.user import User


def test_service():
    # Given
    class FakeRepository(AbstractRepository):
        def get_user(self) -> User:
            return User(name="Faker")

    service = Service(repository=FakeRepository())

    # When
    message = service()

    # Then
    assert message == "Hello, Faker!"
