from fastapi import HTTPException, status


# TODO: Move it from here...
class EntityNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
