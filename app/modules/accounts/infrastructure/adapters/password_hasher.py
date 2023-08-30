from passlib.context import CryptContext

from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.domain.password import Password


class PasswordHasher(AbstractPasswordHasher):
    def __init__(self):
        self._crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: Password) -> str:
        return self._crypt_context.hash(str(password))

    def verify(self, password: Password, hashed_password: str) -> bool:
        try:
            return self._crypt_context.verify(str(password), hashed_password)
        except ValueError:
            return False
