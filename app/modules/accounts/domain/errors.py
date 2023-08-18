from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.errors import EntityNotFoundError


class UserNotFoundError(EntityNotFoundError):
    pass


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: EmailAddress):
        super().__init__(f"A user with the email {email} already exists")
