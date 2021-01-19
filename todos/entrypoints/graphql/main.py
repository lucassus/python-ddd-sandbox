from fastapi import Depends, FastAPI, Request
from starlette.datastructures import URL
from starlette.graphql import GraphQLApp

from todos.entrypoints.graphql.dependencies import get_uow
from todos.entrypoints.graphql.schema import schema
from todos.interfaces.abstract_unit_of_work import AbstractUnitOfWork
from todos.interfaces.db.tables import start_mappers

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
