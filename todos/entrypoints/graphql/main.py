import graphene
from fastapi import FastAPI
from graphene import ObjectType
from starlette.graphql import GraphQLApp

from todos.interfaces.db.tables import start_mappers
from todos.interfaces.db.unit_of_work import UnitOfWork

start_mappers()


class Task(ObjectType):
    id = graphene.ID()
    name = graphene.NonNull(graphene.String)


class Project(ObjectType):
    id = graphene.ID()
    name = graphene.NonNull(graphene.String)
    tasks = graphene.NonNull(graphene.List(Task))


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    projects = graphene.NonNull(graphene.List(graphene.NonNull(Project)))

    def resolve_hello(self, info, name):
        return "Hello " + name

    def resolve_projects(self, info):
        with UnitOfWork() as uof:
            return uof.repository.list()


app = FastAPI()
graphql_app = GraphQLApp(schema=graphene.Schema(query=Query))
app.add_route("/", graphql_app)
