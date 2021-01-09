from datetime import date

from todos.db.session import SessionLocal, engine
from todos.db.tables import metadata, start_mappers
from todos.domain.models import Todo


def seed():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    start_mappers()

    session = SessionLocal()

    session.add(Todo(name="Learn Python", completed_at=date(2021, 1, 9)))
    session.add(Todo(name="Clean house"))
    session.add(Todo(name="Do shopping"))
    session.commit()


if __name__ == "__main__":
    seed()
