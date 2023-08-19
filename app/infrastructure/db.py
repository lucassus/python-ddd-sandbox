from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-an-engine
# The engine is a factory that can create db connections.
# Also holds connections inside a connection pool for fast re-use.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,  # To have SQLAlchemy log every SQL statements issued to the database
    pool_size=5,
    max_overflow=10,  # The maximum number of connections above the pool that can be created during the spike
)

# See https://docs.sqlalchemy.org/en/20/orm/session_api.html#session-and-sessionmaker
# The purpose of sessionmaker is to provide a factory for Session objects with a fixed configuration.
AppSession = sessionmaker(
    autoflush=True,  # Default is True
    autocommit=False,  # Default is False
    # Defaults to True. When True, all instances will be fully expired after each commit(), so that all
    # attribute/object access to a completed transaction will load from the most recent database state.
    expire_on_commit=True,
    # It’s also usually a good idea to set Session.expire_on_commit to False so that subsequent
    # access to objects that came from a Session within the view layer do not need to emit new SQL queries
    # to refresh the objects, if the transaction has been committed already.
    # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
)
