import pytest

from app.modules.accounts.application.testing.fake_user_repository import FakeUserRepository
from app.modules.accounts.application.tracking_user_repository import TrackingUserRepository
from app.modules.accounts.domain.user_builder import UserBuilder
from app.modules.shared_kernel.entities.email_address import EmailAddress


class TestTrackingUserRepository:
    @pytest.fixture()
    def repository(self):
        return TrackingUserRepository(FakeUserRepository())

    def test_seen_is_frozen(self, repository: TrackingUserRepository):
        with pytest.raises(AttributeError):
            repository.seen.add(UserBuilder().build())  # type: ignore

    def test_create(self, repository: TrackingUserRepository):
        user = UserBuilder().build()
        repository.create(user)
        assert user in repository.seen

    def test_get(self, repository: TrackingUserRepository):
        user = UserBuilder().build()
        repository.create(user)

        loaded = repository.get(user.id)
        assert loaded is not None
        assert loaded in repository.seen

    def test_get_by_email(self, repository: TrackingUserRepository):
        user = UserBuilder().with_email("test@email.com").build()
        repository.create(user)

        loaded = repository.get_by_email(EmailAddress(user.email))
        assert loaded is not None
        assert loaded in repository.seen
