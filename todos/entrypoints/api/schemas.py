from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from todos.utils import camelize


class BaseSchema(BaseModel):
    pass

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True


class Project(BaseSchema):
    id: int
    name: str


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)


class Task(BaseSchema):
    id: int
    name: str
    completed_at: Optional[date]
