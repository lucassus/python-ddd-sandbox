from app.modules.accounts.domain.email_address import EmailAddress
from app.modules.accounts.domain.errors import EmailAlreadyExistsException, UserNotFoundError
from app.modules.accounts.domain.ports import AbstractUnitOfWork
from app.shared_kernel.user_id import UserID


class ChangeUserEmailAddress:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    # TODO: This is wrong but unit test does not catch it
    # TODO: Maybe fake UoW impl is not good enough?
    def __call__(self, user_id: UserID, new_email: EmailAddress) -> None:
        with self._uow as uow:
            user = uow.user.get(user_id)

            if user is None:
                raise UserNotFoundError(user_id)

            if user.email == new_email:
                return

            if uow.user.exists_by_email(new_email):
                raise EmailAlreadyExistsException(new_email)

            user.email = new_email
            uow.commit()
