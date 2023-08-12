from typing import Annotated

import pytest
from pydantic import BaseModel, BeforeValidator, ConfigDict

from app.command.accounts.domain.email_address import EmailAddress, InvalidEmailAddressError
from app.command.accounts.domain.password import Password
from app.command.shared_kernel.entities.user_id import UserID

EmailField = Annotated[EmailAddress, BeforeValidator(lambda value: EmailAddress(str(value)))]
PasswordField = Annotated[Password, BeforeValidator(lambda value: Password(str(value)))]


# TODO: Use this technique to pass commands from API endpoints to the application layer
class User(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
    )

    id: UserID
    email: EmailField
    password: PasswordField


def test_pydantic_value_objects():
    user = User(
        id=UserID(1),
        email=EmailAddress("test@email.com"),
        password=Password("password123"),
    )

    assert user.id == 1
    assert str(user.email) == "test@email.com"
    assert str(user.password) == "password123"


def test_pydantic_value_objects_model_validate():
    user = User.model_validate(
        {
            "id": 1,
            "email": "test@email.com",
            "password": "password123",
        }
    )

    assert user.id == 1
    assert str(user.email) == "test@email.com"
    assert str(user.password) == "password123"


def test_pydantic_value_objects_model_validate_when_email_not_valid():
    with pytest.raises(InvalidEmailAddressError):
        User.model_validate(
            {
                "id": 1,
                "email": "test",
                "password": "password123",
            }
        )
