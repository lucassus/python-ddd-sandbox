import os
import uuid
from typing import Self


class UserID(uuid.UUID):
    @classmethod
    def generate(cls) -> Self:
        return cls(bytes=os.urandom(16), version=4)
