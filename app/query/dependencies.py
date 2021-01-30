from databases import Database
from fastapi import Request


def get_database(request: Request) -> Database:
    return request.state.database
