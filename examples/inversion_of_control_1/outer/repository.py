from examples.user import User


class Repository:
    def get_user(self) -> User:
        return User(name="Luke")
