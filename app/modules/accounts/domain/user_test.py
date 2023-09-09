from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID
from app.modules.shared_kernel.events import UserAccountCreated


class TestUser:
    def test_create_user_raises_event(self):
        user = User(
            id=UserID.generate(),
            email=EmailAddress("test@email.com"),
            hashed_password="asdf",
        )

        assert user.events[-1] == UserAccountCreated(user_id=user.id)
