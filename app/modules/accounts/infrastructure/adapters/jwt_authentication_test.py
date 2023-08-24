import pytest

from app.modules.accounts.application.ports.authentication_token import AuthenticationTokenError
from app.modules.accounts.infrastructure.adapters.jwt_authentication import JWTAuthentication
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_datetime


class TestJWTImplementation:
    @pytest.fixture()
    def jwt(self) -> JWTAuthentication:
        return JWTAuthentication(secret_key="test-secret")

    def test_encode_and_decode(self, jwt: JWTAuthentication):
        user_id = UserID.generate()
        token = jwt.encode(user_id=user_id)
        assert isinstance(token, str)

        decoded_user_id = jwt.decode(token=token)
        assert decoded_user_id == user_id

    def test_decode_expired_token(self, jwt: JWTAuthentication):
        user_id = UserID.generate()
        token = jwt.encode(user_id=user_id, now=utc_datetime(1983, 3, 4))
        assert isinstance(token, str)

        with pytest.raises(AuthenticationTokenError):
            jwt.decode(token=token)

    def test_decode_invalid_token(self, jwt: JWTAuthentication):
        with pytest.raises(AuthenticationTokenError):
            jwt.decode("invalid.token.123")
