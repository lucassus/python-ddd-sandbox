from typing import Any

from app.shared.base_value_object import BaseValueObject


class InvalidEmailAddressError(Exception):
    pass


class EmailAddress(BaseValueObject):
    def __init__(self, address: str):
        if not self.is_valid(address):
            raise InvalidEmailAddressError()

        self._address = address

    @staticmethod
    def is_valid(email: str) -> bool:
        return "@" in email

    @property
    def address(self) -> str:
        return self._address

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EmailAddress):
            return False

        return self.address == other.address
