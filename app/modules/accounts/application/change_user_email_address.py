from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.domain.errors import EmailAlreadyExistsException, UserNotFoundError
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class ChangeUserEmailAddress:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

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
