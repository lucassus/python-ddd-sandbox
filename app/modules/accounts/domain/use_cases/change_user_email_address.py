from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException, UserNotFoundError
from app.modules.accounts.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


class ChangeUserEmailAddress:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    # TODO: This is wrong but unit test does not catch it,
    #  consult it with the book
    def __call__(self, user_id: UserID, new_email: EmailAddress):
        user = self._uow.repository.get(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if user.email == new_email:
            return

        if self._uow.repository.exists_by_email(new_email):
            raise EmailAlreadyExistsException(new_email)

        user.email = new_email
        self._uow.commit()
