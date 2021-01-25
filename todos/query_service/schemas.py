from datetime import date
from typing import Optional

from todos.common.base_schema import BaseSchema


class User(BaseSchema):
    id: int
    email: str
    password: str


class Project(BaseSchema):
    id: int
    name: str


class Task(BaseSchema):
    id: int
    name: str
    completed_at: Optional[date]
