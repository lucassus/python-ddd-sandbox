from typing import Annotated, Union

import pytest
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, ValidationError


class InvalidEmailError(ValueError):
    pass


class EmailAddress:
    def __init__(self, address: Union["EmailAddress", str]):
        if "@" not in address:
            raise InvalidEmailError()

        self._address = str(address)

    def __str__(self) -> str:
        return self._address

    def __contains__(self, item: str) -> bool:
        return item in self._address

    def __len__(self) -> int:
        return len(self._address)


EmailField = Annotated[
    EmailAddress,
    BeforeValidator(lambda v: EmailAddress(v)),
    Field(title="Email address", min_length=6, max_length=32),
]


class User(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
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
