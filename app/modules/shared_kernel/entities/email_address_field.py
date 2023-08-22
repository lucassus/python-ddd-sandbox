from typing import Annotated, Any

from pydantic import Field
from pydantic_core import CoreSchema, core_schema

from app.modules.shared_kernel.entities.email_address import EmailAddress, InvalidEmailAddressError


class EmailAddressPydanticAnnotation:
    @classmethod
    def validate(cls, s: Any, validator) -> EmailAddress:
        if isinstance(s, EmailAddress):
            return s

        try:
            return EmailAddress(validator(s))
        except InvalidEmailAddressError as e:
            raise ValueError("Invalid email address") from e  # noqa: TRY003

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> CoreSchema:
        assert source_type is EmailAddress  # noqa: S101

        return core_schema.no_info_wrap_validator_function(
            function=cls.validate,
            schema=core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


# TODO: Is shared_kernel/entities or domain the right place for this?
EmailAddressField = Annotated[
    EmailAddress,
    EmailAddressPydanticAnnotation,
    Field(min_length=6, max_length=32),
]
