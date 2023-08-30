from app.modules.accounts.domain.password import Password
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher


def test_password_hasher():
    hasher = PasswordHasher()

    password = Password("secret-password")
    hashed_password = hasher.hash(password)

    assert str(password) != hashed_password
    assert hasher.verify(password, hashed_password)

    assert not hasher.verify(Password("invalid-password"), hashed_password)
    assert not hasher.verify(password, "asdf")


def test_password_hasher_hash_each_time_generates_different_hash():
    hasher = PasswordHasher()

    password = Password("secret-password")
    assert hasher.hash(password) != hasher.hash(password)
