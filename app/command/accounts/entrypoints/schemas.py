from pydantic import Field

from app.base_schema import BaseSchema

EmailField = Field(..., title="User email address", min_length=4, max_length=32)


class RegisterUser(BaseSchema):
    email: str = EmailField
    password: str = Field(..., min_length=6)


class UpdateUser(BaseSchema):
    email: str = EmailField
