class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        super().__init__(f"A user with the email {email} already exists")
