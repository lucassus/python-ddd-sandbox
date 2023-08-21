from typing import Annotated, Any

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic_core import CoreSchema, core_schema


class InvalidEmailError(Exception):
    pass


class EmailAddress:
    def __init__(self, address: str):
        if "@" not in address:
            raise InvalidEmailError()

        self._address = address

    def __str__(self):
        return self._address


class EmailAddressPydanticAnnotation:
    @classmethod
    def validate_email_address(cls, v: Any, handler) -> EmailAddress:
        if isinstance(v, EmailAddress):
            return v

        s = handler(v)

        try:
            return EmailAddress(s)
        except InvalidEmailError as e:
            raise ValueError("Invalid email address") from e  # noqa: TRY003

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> CoreSchema:
        assert source_type is EmailAddress
        return core_schema.no_info_wrap_validator_function(
            cls.validate_email_address,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


EmailField = Annotated[EmailAddress, EmailAddressPydanticAnnotation]


# TODO: Use this technique to pass commands from API endpoints to the application layer
class User(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=False,
        frozen=True,
    )

    id: int
    email: EmailField
    password: str


def test_pydantic_value_objects():
    user = User(
        id=1,
        email=EmailAddress("test@email.com"),
        password="password",
    )

    assert user.id == 1
    assert str(user.email) == "test@email.com"
    assert user.password == "password"


def test_pydantic_value_objects_model_validate():
    user = User.model_validate(
        {
            "id": 1,
            "email": "test@email.com",
            "password": "password",
        }
    )

    assert user.id == 1
    assert str(user.email) == "test@email.com"
    assert user.password == "password"


def test_pydantic_value_objects_model_validate_when_email_not_valid():
    with pytest.raises(ValidationError):
        User.model_validate(
            {
                "id": 1,
                "email": "test",
                "password": "password",
            }
        )
