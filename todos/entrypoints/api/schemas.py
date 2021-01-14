from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)


class Task(BaseModel):
    id: int
    name: str
    completed_at: Optional[date]

    class Config:
        orm_mode = True
