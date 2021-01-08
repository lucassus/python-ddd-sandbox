from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CreateTodo(BaseModel):
    name: str = Field(..., title="New todo's name", min_length=4, max_length=255)


class Todo(BaseModel):
    id: int
    name: str
    completed_at: Optional[date]

    class Config:
        orm_mode = True
