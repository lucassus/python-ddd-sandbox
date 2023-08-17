from datetime import datetime, timedelta

import jwt

from app.modules.shared_kernel.entities.user_id import UserID
from app.utc_datetime import utc_now


class JWT:
    _algorithm = "HS256"
    _expiration_delta = timedelta(days=90)

    def __init__(self, jwt_secret_key: str):
        self._jwt_secret_key = jwt_secret_key

    def create(self, user_id: UserID, now: datetime | None = None) -> str:
        if now is None:
            now = utc_now()

        return jwt.encode(
            payload={
                "sub": user_id,
                "exp": now + self._expiration_delta,
                "iat": now,
            },
            key=self._jwt_secret_key,
            algorithm=self._algorithm,
        )

    def decode(self, token: str) -> UserID:
        payload = jwt.decode(
            token,
            key=self._jwt_secret_key,
            algorithms=[self._algorithm],
        )

        # TODO: Check if token is expired

        return UserID(payload["sub"])
