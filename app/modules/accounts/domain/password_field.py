from typing import Annotated, Any

from pydantic import Field
from pydantic_core import CoreSchema, core_schema

from app.modules.accounts.domain.password import InvalidPasswordError, Password


class PasswordPydanticAnnotation:
    @classmethod
    def validate(cls, s: Any, validator) -> Password:
        if isinstance(s, Password):
            return s

        try:
            return Password(validator(s))
        except InvalidPasswordError as e:
            raise ValueError("Invalid email address") from e  # noqa: TRY003

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> CoreSchema:
        assert source_type is Password  # noqa: S101

        return core_schema.no_info_wrap_validator_function(
            function=cls.validate,
            schema=core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


PasswordField = Annotated[
    Password,
    PasswordPydanticAnnotation,
    Field(min_length=6),
]
