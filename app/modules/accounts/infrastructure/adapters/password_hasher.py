import bcrypt

from app.modules.accounts.application.ports.abstract_password_hasher import AbstractPasswordHasher
from app.modules.accounts.domain.password import Password

# bcrypt only considers the first 72 bytes of a password and (since 4.x) raises on longer
# inputs. passlib used to silently truncate; we mirror that here in both hash() and verify()
# to preserve behavior and keep existing $2b$ hashes verifiable. Tightening this length-only
# policy is tracked as a separate security change.
_BCRYPT_MAX_BYTES = 72


def _encode(password: Password) -> bytes:
    return str(password).encode("utf-8")[:_BCRYPT_MAX_BYTES]


class PasswordHasher(AbstractPasswordHasher):
    def hash(self, password: Password) -> str:
        hashed_password = bcrypt.hashpw(_encode(password), bcrypt.gensalt())
        return hashed_password.decode("utf-8")

    def verify(self, password: Password, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(_encode(password), hashed_password.encode("utf-8"))
        except ValueError:
            return False
