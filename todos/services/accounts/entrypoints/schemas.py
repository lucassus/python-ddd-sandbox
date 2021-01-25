from pydantic import Field

from todos.common.base_schema import BaseSchema


class RegisterUser(BaseSchema):
    email: str = Field(..., title="User email address", min_length=4, max_length=32)
    password: str = Field(..., min_length=6)
