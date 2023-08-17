import pytest

from app.modules.accounts.application.jwt import JWT, JWTError
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_datetime


class TestJWT:
    @pytest.fixture()
    def jwt(self) -> JWT:
        return JWT(secret_key="test-secret")

    def test_encode_and_decode(self, jwt: JWT):
        user_id = UserID(123)
        token = jwt.encode(user_id=user_id)
        assert isinstance(token, str)

        decoded_user_id = jwt.decode(token=token)
        assert decoded_user_id == user_id

    def test_decode_expired_token(self, jwt: JWT):
        user_id = UserID(123)
        token = jwt.encode(user_id=user_id, now=utc_datetime(1983, 3, 4))
        assert isinstance(token, str)

        with pytest.raises(JWTError):
            jwt.decode(token=token)

    def test_decode_invalid_token(self, jwt: JWT):
        with pytest.raises(JWTError):
            jwt.decode("invalid.token.123")
