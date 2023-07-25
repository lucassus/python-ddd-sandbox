class EmailAddress:
    def __init__(self, address: str):
        if "@" not in address:
            # TODO: Replace it with a custom exception
            raise ValueError("Invalid email address")

        self._address = address

    @property
    def address(self) -> str:
        return self._address

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EmailAddress):
            return False

        return self.address == other.address
