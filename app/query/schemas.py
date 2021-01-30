from datetime import date
from typing import List, Optional

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
    password: str

    projects: List[Project]
