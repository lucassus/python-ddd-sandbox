import pytest

from app.modules.accounts.domain.email_address import EmailAddress


class TestEmailAddress:
    def test_when_invalid_raises_error(self):
        with pytest.raises(ValueError):
            EmailAddress("invalid")

    def test_when_valid(self):
        email = EmailAddress("test@email.com")
        assert email.address == "test@email.com"

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
