from datetime import date
from typing import Optional

from app.common.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class Task(BaseSchema):
    id: int
    name: str
    completed_at: Optional[date]


class User(BaseSchema):
    id: int
    email: str

    projects: list[Project]
