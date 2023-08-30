from app.modules.accounts.application.password import get_password_hash
from app.modules.accounts.domain.password import Password
from app.modules.accounts.domain.user import User
from app.modules.shared_kernel.entities.email_address import EmailAddress
from app.modules.shared_kernel.entities.user_id import UserID


class TestUser:
    def test_create_user_raises_event(self):
        user = User(
            id=UserID.generate(),
            email=EmailAddress("test@email.com"),
            hashed_password=get_password_hash(Password("password")),
        )

        assert user.events[-1] == User.AccountCreated(user_id=user.id)
