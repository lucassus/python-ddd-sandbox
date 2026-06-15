from app.modules.accounts.domain.password import Password
from app.modules.accounts.infrastructure.adapters.password_hasher import PasswordHasher

# A $2b$ hash produced by the previous passlib-based hasher (bcrypt scheme, 12 rounds)
# for the plaintext "secret-password". Verifying it proves backward compatibility.
PASSLIB_ERA_HASH = "$2b$12$EoKatZar06UMnARZd4I7LuiKdyyUP.0vzYaKGdWprF4b3PJsUR21a"


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


def test_password_hasher_verifies_a_preexisting_passlib_hash():
    hasher = PasswordHasher()

    assert hasher.verify(Password("secret-password"), PASSLIB_ERA_HASH)
    assert not hasher.verify(Password("wrong-password"), PASSLIB_ERA_HASH)


def test_password_hasher_handles_passwords_longer_than_72_bytes():
    hasher = PasswordHasher()

    password = Password("a" * 100)
    hashed_password = hasher.hash(password)

    assert hasher.verify(password, hashed_password)
