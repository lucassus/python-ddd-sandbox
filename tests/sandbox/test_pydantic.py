from typing import Annotated, Any

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError, Field
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

    def __len__(self):
        return len(self._address)


def validate_email_address(
    s: Any,
    validator: core_schema.ValidatorFunctionWrapHandler,
) -> EmailAddress:
    if isinstance(s, EmailAddress):
        return s

    try:
        return EmailAddress(validator(s))
    except InvalidEmailError as e:
        raise ValueError("Invalid email address") from e  # noqa: TRY003


class EmailAddressPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> CoreSchema:
        assert source_type is EmailAddress

        return core_schema.no_info_wrap_validator_function(
            function=validate_email_address,
            schema=core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )


EmailField = Annotated[
    EmailAddress,
    EmailAddressPydanticAnnotation,
    Field(title="Email address", min_length=6, max_length=32),
]


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

    User.model_validate(
        {
            "id": 1,
            "email": EmailAddress("test@email.com"),
            "password": "password",
        }
    )


def test_pydantic_value_objects_model_validate_when_email_not_valid():
    with pytest.raises(ValidationError):
        User.model_validate(
            {
                "id": 1,
                "email": "test",
                "password": "password",
            }
        )

    with pytest.raises(ValidationError):
        User.model_validate(
            {
                "id": 1,
                "email": "a@b.c",
                "password": "password",
            }
        )
