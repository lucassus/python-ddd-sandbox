from app.modules.accounts.application.testing.fake_password_hasher import FakePasswordHasher
from app.modules.accounts.domain.password import Password


def test_fake_password_hasher():
    hasher = FakePasswordHasher()

    password = Password("secret-password")
    hashed_password = hasher.hash(password)

    assert str(password) != hashed_password
    assert hasher.verify(password, hashed_password)
