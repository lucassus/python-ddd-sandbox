from typing import Callable, Self

from sqlalchemy.orm import Session

from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.infrastructure.adapters.user_repository import UserRepository
from app.modules.shared_kernel.message_bus import MessageBus


class UnitOfWork(AbstractUnitOfWork):
    repository: UserRepository

    def __init__(self, session_factory: Callable[..., Session], bus: MessageBus):
        super().__init__(bus=bus)
        self._session_factory = session_factory

    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self.user = UserRepository(session=self._session)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

        for user in self.user.seen:
            for event in user.events:
                self._bus.dispatch(event)

            user.events.clear()

    def rollback(self):
        self._session.rollback()
