import os
import sys

database_path = os.path.join(
    os.path.dirname(__file__),
    "../todos.db" if "pytest" not in sys.modules else "../todos_test.db",
)
DATABASE_URL = f"sqlite:///{database_path}"
