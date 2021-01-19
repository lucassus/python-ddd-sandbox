from examples.inversion_of_control_3.inner.abstract_repository import AbstractRepository


class Service:
    def __init__(self, repository: AbstractRepository):
        self._repository = repository

    def __call__(self, *args, **kwargs):
        user = self._repository.get_user()
        return f"Hello, {user.name}!"
