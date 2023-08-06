from datetime import datetime
from typing import Optional

from app.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class Task(BaseSchema):
    number: int
    name: str
    completed_at: Optional[datetime] = None


class User(BaseSchema):
    id: int
    email: str

    projects: list[Project]
