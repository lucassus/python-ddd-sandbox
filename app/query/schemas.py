from datetime import datetime
from typing import Optional

from app.command.shared_kernel.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class Task(BaseSchema):
    number: int
    name: str
    completed_at: Optional[datetime] = None
