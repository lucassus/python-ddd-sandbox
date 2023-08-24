import os
import uuid


# TODO: Create a base class
class UserID(uuid.UUID):
    @classmethod
    def generate(cls) -> "UserID":
        return cls(bytes=os.urandom(16), version=4)
