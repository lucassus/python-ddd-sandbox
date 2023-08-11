from pydantic import Field

from app.base_schema import BaseSchema

# TODO: Move it to application layer?
# TODO: ...and do the same for projects


class RegisterUser(BaseSchema):
    email: str = Field(..., title="User email address", min_length=4, max_length=32)
    password: str = Field(..., min_length=6)


class UpdateUser(BaseSchema):
    email: str = Field(..., title="User email address", min_length=4, max_length=32)
