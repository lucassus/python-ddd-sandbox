from datetime import datetime
from typing import Optional

from pydantic import Field

from app.command.shared_kernel.base_schema import BaseSchema


class CreateProject(BaseSchema):
    user_id: int = Field(..., title="User's ID")
    name: str = Field(..., title="New project's name", min_length=4, max_length=32)


class UpdateProject(BaseSchema):
    name: str = Field(..., title="New project's name", min_length=4, max_length=32)


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)


# TODO: These are for queries, move to abstract classes


class Project(BaseSchema):
    id: int
    name: str


class Task(BaseSchema):
    number: int
    name: str
    completed_at: Optional[datetime] = None
