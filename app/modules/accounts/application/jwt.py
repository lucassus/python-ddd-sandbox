from datetime import datetime, timedelta

import jwt
from jwt import DecodeError, ExpiredSignatureError

from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


class JWTError(Exception):
    pass


# TODO: Create an interface for this class
class JWT:
    _algorithm = "HS256"
    _expiration_delta = timedelta(days=90)

    def __init__(self, secret_key: str):
        self._secret_key = secret_key

    def encode(self, user_id: UserID, now: datetime | None = None) -> str:
        if now is None:
            now = utc_now()

        return jwt.encode(
            payload={
                "sub": user_id,
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
            raise JWTError() from e

        return UserID(payload["sub"])
