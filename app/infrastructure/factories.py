from datetime import date
from typing import Any, Optional

from faker import Faker
from sqlalchemy import Connection

from app.infrastructure.tables import projects_table, tasks_table, users_table

fake = Faker()
fake.seed_instance(667)


def _build_user(
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> dict[str, Any]:
    if email is None:
        email = fake.email()

    if password is None:
        password = fake.password()

    return {"email": email, "password": password}


def create_user(
    connection: Connection,
    email: Optional[str] = None,
    password: Optional[str] = None,
):
    user = connection.execute(
        users_table.insert().values(_build_user(email=email, password=password)).returning(users_table)
    ).first()

    return user


def _build_project(
    user_id: Optional[int] = None,
    name: Optional[str] = None,
) -> dict[str, Any]:
    if name is None:
        name = fake.word()

    return {"user_id": user_id, "name": name}


def create_project(
    connection: Connection,
    user_id: Optional[int] = None,
    name: Optional[str] = None,
):
    if user_id is None:
        user_id = create_user(connection).id

    project = connection.execute(
        projects_table.insert().values(_build_project(user_id=user_id, name=name)).returning(projects_table)
    ).first()

    return project


def _build_task(
    project_id: int,
    number: int,
    name: Optional[str] = None,
    completed_at: Optional[date] = None,
) -> dict[str, Any]:
    if name is None:
        name = fake.word()

    return {
        "project_id": project_id,
        "number": number,
        "name": name,
        "completed_at": completed_at,
    }


def create_task(
    connection: Connection,
    number: int,
    project: Optional[Any] = None,
    name: Optional[str] = None,
    completed_at: Optional[date] = None,
):
    if project is None:
        project = create_project(connection)

    task = connection.execute(
        tasks_table.insert()
        .values(
            _build_task(
                project_id=project.id,
                number=number,
                name=name,
                completed_at=completed_at,
            )
        )
        .returning(tasks_table)
    ).first()

    return task
