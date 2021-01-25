from todos.services.accounts.domain.entities import User
from todos.services.accounts.domain.ports import AbstractUnitOfWork


class Service:
    def __init__(self, *, uow: AbstractUnitOfWork):
        self._uow = uow

    def register_user(self, *, email: str, password: str) -> int:
        with self._uow as uow:
            user = User(email=email, password=password)
            uow.repository.create(user)
            uow.commit()

            return user.id
