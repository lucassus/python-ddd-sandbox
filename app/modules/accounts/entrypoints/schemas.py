from app.modules.accounts.domain.password_field import PasswordField
from app.shared.base_schema import BaseSchema
from app.shared.email_address_field import EmailAddressField


class RegisterUser(BaseSchema):
    email: EmailAddressField
    password: PasswordField


class LoginUser(BaseSchema):
    email: EmailAddressField
    password: PasswordField


class UpdateUser(BaseSchema):
    email: EmailAddressField
