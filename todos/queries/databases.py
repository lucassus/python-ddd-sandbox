from databases import Database

from todos.adapters.sqlalchemy.config import DB_URL

database = Database(DB_URL)
