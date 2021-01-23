import os

db_file = os.path.join(os.path.dirname(__file__), "../todos.db")
DB_URL = f"sqlite:///{db_file}"
