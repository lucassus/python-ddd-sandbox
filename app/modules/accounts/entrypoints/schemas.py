from app.modules.accounts.domain.password_field import PasswordField
from app.modules.shared_kernel.base_schema import BaseSchema
from app.modules.shared_kernel.entities.email_address_field import EmailAddressField


class RegisterUser(BaseSchema):
    email: EmailAddressField
    password: PasswordField


class UpdateUser(BaseSchema):
    email: EmailAddressField


class LoginUser(BaseSchema):
    email: EmailAddressField
    password: PasswordField
