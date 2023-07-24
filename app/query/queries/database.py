from databases import Database
from starlette.requests import Request


# TODO: Find a better place?
def get_database(request: Request) -> Database:
    return request.state.database
