from unittest.mock import Mock

from app.infrastructure.message_bus import MessageBus
from app.modules.accounts.application.ports.abstract_user_repository import AbstractUserRepository
from app.modules.accounts.application.ports.tracking_user_repository import TrackingUserRepository
from app.modules.accounts.application.testing.fake_unit_of_work import FakeUnitOfWork
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.events import UserAccountCreated
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


def test_unit_of_work_commit(repository: AbstractUserRepository, message_bus: MessageBus):
    # Given
    account_created_mock = Mock()
    message_bus.listen(UserAccountCreated, account_created_mock)

    uow = FakeUnitOfWork(
        repository=TrackingUserRepository(repository),
        bus=message_bus,
    )

    # When
    user_id = UserID.generate()

    with uow:
        uow.users.create(
            User(
                id=user_id,
                email=EmailAddress("test@email.com"),
                hashed_password="asdf",
            )
        )

        uow.commit()

    # Then
    assert uow.committed is True
    assert len(uow.users.seen) == 1

    assert account_created_mock.call_count == 1
    account_created_mock.assert_called_with(UserAccountCreated(user_id=user_id))
