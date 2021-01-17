from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from todos.utils import camelize


class Project(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CreateTask(BaseModel):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)


# TODO: Create a base class for camelized schemas
class Task(BaseModel):
    id: int
    name: str
    completed_at: Optional[date]

    class Config:
        orm_mode = True
        alias_generator = camelize
        allow_population_by_field_name = True
