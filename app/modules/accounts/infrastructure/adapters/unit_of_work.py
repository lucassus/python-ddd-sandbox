from typing import Callable, Self

from sqlalchemy.orm import Session

from app.infrastructure.message_bus import MessageBus
from app.modules.accounts.application.ports.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.accounts.application.ports.tracking_user_repository import TrackingUserRepository
from app.modules.accounts.infrastructure.adapters.user_repository import UserRepository


class UnitOfWork(AbstractUnitOfWork):
    repository: TrackingUserRepository

    def __init__(self, session_factory: Callable[..., Session], bus: MessageBus):
        super().__init__(bus=bus)
        self._session_factory = session_factory

    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self.users = TrackingUserRepository(UserRepository(session=self._session))

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def _commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
