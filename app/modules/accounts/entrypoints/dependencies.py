from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from app.modules.accounts.entrypoints.containers import Container


@inject
def get_authentication(container: Container = Depends(Provide[Container])):
    return container.application.authentication()
