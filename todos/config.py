import os
import sys

db_file = os.path.join(
    os.path.dirname(__file__),
    "../todos.db" if "pytest" not in sys.modules else "../todos_test.db",
)
DB_URL = f"sqlite:///{db_file}"
