from pydantic import Field

from app.modules.shared_kernel.base_schema import BaseSchema

EmailField = Field(..., title="User email address", min_length=4, max_length=32)
PasswordField = Field(..., min_length=6)


class RegisterUser(BaseSchema):
    email: str = EmailField
    password: str = PasswordField


class UpdateUser(BaseSchema):
    email: str = EmailField


class LoginUser(BaseSchema):
    email: str = EmailField
    password: str = PasswordField
