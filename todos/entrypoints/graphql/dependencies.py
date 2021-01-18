from todos.interfaces.db.unit_of_work import UnitOfWork


def get_uow():
    with UnitOfWork() as uow:
        yield uow
