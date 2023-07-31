from pydantic import BaseModel


def camelize(str: str) -> str:
    return "".join([char.upper() if str[i - 1] == "_" else char for i, char in enumerate(str) if char != "_"])


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
