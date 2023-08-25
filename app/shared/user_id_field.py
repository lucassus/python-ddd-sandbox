from typing import Annotated

from pydantic import BeforeValidator
from pydantic.types import UUID4

UserIDField = Annotated[UUID4, BeforeValidator(lambda v: str(v))]
