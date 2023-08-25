import uuid


class UserID:
    def __init__(self, id: str | bytes | uuid.UUID) -> None:
        if isinstance(id, uuid.UUID):
            self._uuid = id
        else:
            self._uuid = uuid.UUID(str(id))

    @classmethod
    def generate(cls) -> "UserID":
        return cls(uuid.uuid4())

    def __str__(self):
        return str(self._uuid)

    def __eq__(self, other):
        return isinstance(other, UserID) and self._uuid == other._uuid

    def __hash__(self):
        return hash(self._uuid)
