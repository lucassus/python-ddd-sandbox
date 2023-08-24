from datetime import datetime

import jwt
from jwt import DecodeError, ExpiredSignatureError

from app.modules.accounts.application.ports.authentication_token import AuthenticationToken, AuthenticationTokenError
from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


class JWTAuthentication(AuthenticationToken):
    _algorithm = "HS256"

    def encode(self, user_id: UserID, now: datetime | None = None) -> str:
        if now is None:
            now = utc_now()

        return jwt.encode(
            payload={
                "sub": str(user_id),
                "exp": now + self._expiration_delta,
                "iat": now,
            },
            key=self._secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> UserID:
        try:
            payload = jwt.decode(
                token,
                key=self._secret_key,
                algorithms=[self._algorithm],
            )
        except (DecodeError, ExpiredSignatureError) as e:
            raise AuthenticationTokenError() from e

        return UserID(payload["sub"])
