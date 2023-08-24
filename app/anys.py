import uuid


class _AnyUUID:
    def __eq__(self, other):
        try:
            uuid.UUID(str(other))
        except ValueError:
            return False
        else:
            return True


AnyUUID = _AnyUUID()
