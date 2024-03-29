from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.domain.password import Password


class FakePasswordHasher(AbstractPasswordHasher):
    def hash(self, password: Password) -> str:
        return str(password)[::-1]

    def verify(self, password: Password, hashed_password: str) -> bool:
        return str(password)[::-1] == hashed_password
