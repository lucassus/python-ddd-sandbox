from pydantic import BaseModel, ConfigDict


def camelize(str: str) -> str:
    return "".join([char.upper() if str[i - 1] == "_" else char for i, char in enumerate(str) if char != "_"])


# TODO: Move it to shared kernel
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=camelize,
        populate_by_name=True,
    )
