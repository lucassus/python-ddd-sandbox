from typing import Any

from app.command.shared_kernel.entities.value_object import ValueObject


class InvalidPasswordError(Exception):
    pass


class Password(ValueObject):
    def __init__(self, value: str) -> None:
        if not self.is_valid(value):
            raise InvalidPasswordError()

        self._value = value

    @staticmethod
    def is_valid(password: str) -> bool:
        return len(password) >= 8

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Password):
            return False

        return self.value == other.value
