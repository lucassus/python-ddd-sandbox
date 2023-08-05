from typing import Any

from email_validator import EmailNotValidError, validate_email

from app.command.shared_kernel.entities.value_object import ValueObject


class InvalidEmailAddressError(Exception):
    pass


class EmailAddress(ValueObject):
    def __init__(self, address: str):
        if not self.is_valid(address):
            raise InvalidEmailAddressError()

        self._address = address

    @staticmethod
    def is_valid(email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @property
    def address(self) -> str:
        return self._address

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmailAddress):
            return False

        return self.address == other.address

    def __str__(self) -> str:
        return self.address
