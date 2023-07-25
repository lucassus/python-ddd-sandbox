import pytest

from app.modules.accounts.domain.password import InvalidPasswordError, Password


class TestPassword:
    def test_initialize_with_valid_password(self):
        password = Password("password")

        assert password.value == "password"

    def test_initialize_with_invalid_password(self):
        with pytest.raises(InvalidPasswordError):
            Password("pass")

    def test_str(self):
        password = Password("password")
        assert str(password) == "password"

    @pytest.mark.parametrize(
        "left,right,expected",
        [
            (Password("password"), Password("password"), True),
            (Password("password"), Password("password1"), False),
            (Password("password"), "password", False),
        ],
    )
    def test_eq(self, left, right, expected):
        assert (left == right) == expected
