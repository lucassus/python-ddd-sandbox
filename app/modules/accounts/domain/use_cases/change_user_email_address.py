from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import UserNotFoundError
from app.modules.accounts.domain.ports import AbstractUnitOfWork


class ChangeUserEmailAddress:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    # TODO: This is wrong but unit test does not catch it,
    #  consult it with the book
    def __call__(self, user_id: int, new_email: EmailAddress):
        user = self._uow.repository.get(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if user.email == new_email:
            return

        if self._uow.repository.exists_by_email(new_email):
            # TODO: Add a more concrete exception
            raise Exception(f"Email {new_email} is already taken")

        user.email = new_email
        self._uow.commit()
