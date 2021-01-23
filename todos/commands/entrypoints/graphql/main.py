from fastapi import Depends, FastAPI, Request
from starlette.datastructures import URL
from starlette.graphql import GraphQLApp

from todos.commands.adapters.sqlalchemy.mappers import start_mappers
from todos.commands.domain.ports import AbstractUnitOfWork
from todos.commands.entrypoints.graphql.dependencies import get_uow
from todos.commands.entrypoints.graphql.schema import schema

start_mappers()


app = FastAPI()
graphql_app = GraphQLApp(schema=schema)


@app.get("/")
async def graphiql(request: Request):
    request._url = URL("/gql")
    return await graphql_app.handle_graphiql(request=request)


@app.post("/gql")
async def graphql(request: Request, uow: AbstractUnitOfWork = Depends(get_uow)):
    request.state.uow = uow
    return await graphql_app.handle_graphql(request=request)
