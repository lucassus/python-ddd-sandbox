import pytest

from app.modules.accounts.application.jwt import JWT, JWTError


class TestJWT:
    @pytest.fixture()
    def jwt(self) -> JWT:
        return JWT(secret_key="test-secret")

    def test_decode_invalid_token(self, jwt: JWT):
        with pytest.raises(JWTError):
            jwt.decode("invalid.token.123")
