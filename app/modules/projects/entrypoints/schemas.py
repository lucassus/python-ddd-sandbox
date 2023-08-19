from pydantic import Field

from app.modules.shared_kernel.base_schema import BaseSchema


class CreateProject(BaseSchema):
    name: str = Field(..., title="New project's name", min_length=4, max_length=32)


class UpdateProject(BaseSchema):
    name: str = Field(..., title="New project's name", min_length=4, max_length=32)


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)
