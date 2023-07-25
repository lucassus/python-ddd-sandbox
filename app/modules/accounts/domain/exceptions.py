from app.modules.accounts.domain.email_address import EmailAddress


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: EmailAddress):
        super().__init__(f"A user with the email {email} already exists")
