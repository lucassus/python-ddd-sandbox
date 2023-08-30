from passlib.context import CryptContext

from app.modules.accounts.domain.password import Password

_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: Password, hashed_password):
    return _crypt_context.verify(str(password), hashed_password)


# TODO: This is super slow, figure out how to stub it in tests
def get_password_hash(password: Password) -> str:
    return _crypt_context.hash(str(password))
