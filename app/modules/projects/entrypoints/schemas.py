from pydantic import Field

from app.shared.base_schema import BaseSchema


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)
