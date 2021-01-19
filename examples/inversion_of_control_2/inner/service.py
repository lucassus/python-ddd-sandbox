from examples.inversion_of_control_2.outer.repository import Repository


class Service:
    def __init__(self, *, repository: Repository):
        self._repository = repository

    def __call__(self, *args, **kwargs):
        user = self._repository.get_user()
        return f"Hello, {user.name}!"
