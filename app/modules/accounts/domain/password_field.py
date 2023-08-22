from typing import Annotated

from pydantic import Field

# TODO: Add pydantic wrapper, like for email address
PasswordField = Annotated[
    str,
    Field(min_length=6),
]
