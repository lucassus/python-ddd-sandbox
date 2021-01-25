from pydantic import BaseModel

from todos.common.utils import camelize


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
