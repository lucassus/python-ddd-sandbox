from graphene import ID, Boolean, Field, List, Mutation, NonNull, ObjectType, Schema, String

from todos.domain.errors import MaxIncompleteTasksNumberIsReached
from todos.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from todos.service_layer.service import Service


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


class CreateTask(Mutation):
    class Arguments:
        project_id = NonNull(ID)
        name = NonNull(String)

    ok = NonNull(Boolean)
    task = Field(Task)

    def mutate(root, info, project_id: int, name: str):
        uow: AbstractUnitOfWork = info.context["request"].state.uow
        service = Service(project_id=project_id, uow=uow)

        project = uow.repository.get(project_id)
        if project is None:
            return CreateTask(ok=False)

        try:
            task = service.create_task(name)

            return CreateTask(ok=True, task=task)
        except MaxIncompleteTasksNumberIsReached:
            return CreateTask(ok=False)


class Mutations(ObjectType):
    create_task = CreateTask.Field()


schema = Schema(query=Query, mutation=Mutations)
