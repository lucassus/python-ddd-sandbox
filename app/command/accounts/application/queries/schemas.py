from app.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class UserDetails(BaseSchema):
    id: int
    email: str
    projects: list[Project]
