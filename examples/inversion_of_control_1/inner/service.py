from examples.inversion_of_control_1.outer.repository import Repository


class Service:
    def __init__(self):
        self._repository = Repository()

    def __call__(self, *args, **kwargs):
        user = self._repository.get_user()
        return f"Hello, {user.name}!"
