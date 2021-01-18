from graphene import ID, Boolean, List, NonNull, ObjectType, String

from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork


class Task(ObjectType):
    id = ID()
    name = NonNull(String)
    is_completed = NonNull(Boolean)


class Project(ObjectType):
    id = ID()
    name = NonNull(String)
    tasks = NonNull(List(Task))


class Query(ObjectType):
    projects = NonNull(List(NonNull(Project)))

    def resolve_projects(self, info):
        uow: AbstractUnitOfWork = info.context["request"].state.uow
        return uow.repository.list()
