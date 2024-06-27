import asyncio
from typing import Any
from unittest.mock import ANY, Mock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.anys import AnyUUID
from app.modules.projects.application.commands import (
    ArchiveProject,
    CreateProject,
    DeleteProject,
    UnarchiveProject,
    UpdateProject,
)
from app.modules.projects.domain.project import ProjectID, ProjectName
from app.modules.projects.infrastructure.containers import Container
from app.shared.message_bus import MessageBus


@pytest.mark.asyncio
async def test_create_project_endpoint(container: Container, app: FastAPI, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)
    bus_mock.execute.return_value = ProjectID(1)

    # When
    with container.bus.override(bus_mock):
        response = await client.post(
            "/projects",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/1"
    bus_mock.execute.assert_called_with(
        CreateProject(
            user_id=AnyUUID,  # type: ignore
            name=ProjectName("Test project"),
        )
    )


@pytest.mark.asyncio
async def test_list_projects_endpoint(container: Container, client: AsyncClient):
    # Given
    future = asyncio.Future[dict[Any, Any]]()
    future.set_result(
        {
            "projects": [
                {"id": 1, "name": "Test project"},
                {"id": 2, "name": "Test project 2"},
            ]
        }
    )
    list_projects_query_mock = Mock(return_value=future)

    # When
    with container.queries.list_projects_handler.override(list_projects_query_mock):
        response = await client.get("/projects")

    # Then
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_project_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = await client.put(
            "/projects/123",
            json={"name": "Test project"},
            follow_redirects=False,
        )

    # Then
    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.headers["location"] == "/api/projects/123"
    bus_mock.execute.assert_called_with(
        UpdateProject(
            project_id=ProjectID(123),
            name=ProjectName("Test project"),
        )
    )


@pytest.mark.asyncio
async def test_archive_project_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = await client.put("/projects/123/archive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(
        ArchiveProject(
            project_id=ProjectID(123),
            now=ANY,
        )
    )


@pytest.mark.asyncio
async def test_unarchive_project_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = await client.put("/projects/124/unarchive")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(UnarchiveProject(project_id=ProjectID(124)))


@pytest.mark.asyncio
async def test_delete_project_endpoint(container: Container, client: AsyncClient):
    # Given
    bus_mock = Mock(spec=MessageBus)

    # When
    with container.bus.override(bus_mock):
        response = await client.delete("/projects/124")

    # Then
    assert response.status_code == status.HTTP_200_OK
    bus_mock.execute.assert_called_with(DeleteProject(project_id=ProjectID(124), now=ANY))
