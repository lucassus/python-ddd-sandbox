from typing import Any, Union

from email_validator import EmailNotValidError, validate_email

from app.modules.shared_kernel.entities.value_object import ValueObject


class InvalidEmailAddressError(Exception):
    pass


class EmailAddress(ValueObject):
    def __init__(self, address: Union["EmailAddress", str]) -> None:
        if not self.is_valid(str(address)):
            raise InvalidEmailAddressError()

        self._address = str(address)

    @staticmethod
    def is_valid(email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            return False
        else:
            return True

    def __str__(self) -> str:
        return self._address

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmailAddress):
            return False

        return self._address == other._address

    def __len__(self) -> int:
        return len(self._address)
