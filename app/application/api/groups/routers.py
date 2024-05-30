from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.groups.filters import GetGroupsFilters
from application.api.schemas import SErrorMessage
from application.api.groups.schemas import (
    SCreateGroupIn,
    SCreateGroupOut,
    SGetGroup,
    SGetGroupsQueryResponse,
)
from application.api.users.filters import GetUsersFilters
from application.api.users.schemas import SGetUser, SGetUsersQueryResponse
from domain.exceptions.base import ApplicationException
from domain.exceptions.groups import InvalidGroupTitleLength
from logic.commands.groups import (
    CreateGroupCommand,
    DeleteGroupCommand,
)
from logic.exceptions.groups import GroupAlreadyExistsException, GroupNotFoundException
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.groups import (
    GetGroupQuery,
    GetGroupsQuery,
)
from logic.queries.users import GetUsersQuery

group_router = APIRouter()


@group_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateGroupOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_409_CONFLICT: {"model": GroupAlreadyExistsException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": InvalidGroupTitleLength},
    },
)
async def create_group(
    group_in: SCreateGroupIn, container: Annotated[Container, Depends(init_container)]
) -> SCreateGroupOut:
    """Create new user group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        group, *_ = await mediator.handle_command(
            CreateGroupCommand(title=group_in.title)
        )
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return SCreateGroupOut.from_entity(group)


@group_router.get(
    "/{group_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetGroup},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": GroupNotFoundException},
    },
)
async def get_group(
    group_oid: str,
    container: Annotated[Container, Depends(init_container)],
):
    """Get user group info."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        group = await mediator.handle_query(GetGroupQuery(group_oid=group_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetGroup.from_entity(group)


@group_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetGroupsQueryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def get_groups(
    container: Annotated[Container, Depends(init_container)],
    filters: GetGroupsFilters = Depends(),
):
    """Get all groups."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        groups, count = await mediator.handle_query(
            GetGroupsQuery(filters=filters.to_infrastructure_filters())
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetGroupsQueryResponse(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[SGetGroup.from_entity(group) for group in groups],
    )


@group_router.get(
    "/{group_oid}/users/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUsersQueryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": GroupNotFoundException},
    },
)
async def get_users(
    group_oid: str,
    container: Annotated[Container, Depends(init_container)],
    filters: GetUsersFilters = Depends(),
) -> SGetUsersQueryResponse:
    """Get all users from specified group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        users, count = await mediator.handle_query(
            GetUsersQuery(
                group_oid=group_oid, filters=filters.to_infrastructure_filters()
            )
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetUsersQueryResponse(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[SGetUser.from_entity(user) for user in users],
    )


@group_router.delete(
    "/{group_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": GroupNotFoundException},
    },
)
async def delete_group(
    group_oid: str,
    container: Annotated[Container, Depends(init_container)],
) -> None:
    """Delete user group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteGroupCommand(group_oid=group_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
