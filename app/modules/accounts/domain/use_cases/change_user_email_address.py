from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import UserNotFoundError
from app.modules.accounts.domain.ports import AbstractUnitOfWork


class ChangeUserEmailAddress:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def __call__(self, user_id: int, new_email: EmailAddress):
        # TODO: This is wrong but unit test does not catch it,
        #  consult it with the book
        user = self._uow.repository.get(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        user.email = new_email
        self._uow.commit()
