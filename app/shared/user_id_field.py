from typing import Annotated

from pydantic.types import UuidVersion

from app.modules.shared_kernel.entities.user_id import UserID

UserIDField = Annotated[UserID, UuidVersion(4)]
