import os
import uuid
from typing import Self


# TODO: Create a base class
class UUID(uuid.UUID):
    @classmethod
    def generate(cls) -> Self:
        return cls(bytes=os.urandom(16), version=4)


class UserID(UUID):
    pass
