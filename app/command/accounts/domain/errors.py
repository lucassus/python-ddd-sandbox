from app.command.accounts.domain.email_address import EmailAddress
from app.command.shared_kernel.errors import EntityNotFoundError


class UserNotFoundError(EntityNotFoundError):
    pass


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: EmailAddress):
        super().__init__(f"A user with the email {email} already exists")
