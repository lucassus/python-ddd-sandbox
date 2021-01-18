from graphene import ID, Boolean, Field, List, NonNull, ObjectType, String

from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork


class Task(ObjectType):
    id = ID()
    name = NonNull(String)
    is_completed = NonNull(Boolean)
    completed_at = String()


class Project(ObjectType):
    id = ID()
    name = NonNull(String)
    tasks = NonNull(List(NonNull(Task)))


class Query(ObjectType):
    projects = NonNull(List(NonNull(Project)))
    project = Field(NonNull(Project), id=ID())

    def resolve_projects(self, info):
        uow: AbstractUnitOfWork = info.context["request"].state.uow
        return uow.repository.list()

    def resolve_project(self, info, id):
        uow: AbstractUnitOfWork = info.context["request"].state.uow
        return uow.repository.get(id)
