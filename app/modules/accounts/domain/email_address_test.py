import pytest

from app.modules.accounts.domain.email_address import EmailAddress, InvalidEmailAddressError


class TestEmailAddress:
    def test_when_invalid_raises_error(self):
        with pytest.raises(InvalidEmailAddressError):
            EmailAddress("invalid")

    def test_when_valid(self):
        email = EmailAddress("test@email.com")
        assert email.address == "test@email.com"

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("invalid", False),
            ("invalid@", False),
            ("invalid@invalid", False),
            ("invalid@invalid.", False),
            ("valid@email.c", True),
            ("valid+aliasd@email.com", True),
            ("valid.foo@email.com", True),
        ],
    )
    def test_is_valid(self, email: str, expected: bool):
        assert EmailAddress.is_valid(email) == expected

    @pytest.mark.parametrize(
        "left,right,expected",
        [
            (EmailAddress("first@email.com"), EmailAddress("first@email.com"), True),
            (EmailAddress("first@email.com"), EmailAddress("second@email.com"), False),
            (EmailAddress("first@email.com"), "not@email.com", False),
        ],
    )
    def test_equals_returns(self, left: EmailAddress, right: EmailAddress, expected: bool):
        assert (left == right) == expected

    def test_str(self):
        email = EmailAddress("some@email.com")
        assert str(email) == "some@email.com"
