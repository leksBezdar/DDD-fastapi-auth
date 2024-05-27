from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.schemas import SErrorMessage
from application.api.users.filters import GetUsersFilters
from application.api.users.schemas import (
    SCreateGroupIn,
    SCreateGroupOut,
    SCreateUserIn,
    SCreateUserOut,
    SGetGroup,
    SGetGroupsQueryResponse,
    SGetUser,
    SGetUsersQueryResponse,
    SLoginIn,
    SLoginOut,
)
from domain.exceptions.base import ApplicationException
from logic.commands.users import (
    CreateGroupCommand,
    CreateUserCommand,
    DeleteGroupCommand,
    UserLoginCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.users import (
    GetGroupQuery,
    GetGroupsQuery,
    GetUserQuery,
    GetUsersQuery,
)


group_router = APIRouter()
user_router = APIRouter()


@group_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateGroupOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateGroupOut.from_entity(group)


@user_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SLoginOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def login(
    login_data: SLoginIn, container: Annotated[Container, Depends(init_container)]
) -> SLoginOut:
    """User login."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            UserLoginCommand(username=login_data.username, password=login_data.password)
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SLoginOut.from_entity(user)


@user_router.post(
    "/{group_oid}/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateUserOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def create_user(
    group_oid: str,
    user_in: SCreateUserIn,
    container: Annotated[Container, Depends(init_container)],
) -> SCreateUserOut:
    """Create new user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(
                email=user_in.email,
                username=user_in.username,
                password=user_in.password,
                group_oid=group_oid,
            )
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateUserOut.from_entity(user)


@group_router.get(
    "/{group_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetGroup},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
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
    filters: GetUsersFilters = Depends(),
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


@group_router.delete(
    "/{group_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage}},
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


@user_router.get(
    "/{group_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUsersQueryResponse},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
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


@user_router.get("/verify/{token}/")
async def verify_user(
    token: str,
    container: Annotated[Container, Depends(init_container)],
) -> bool:
    mediator: Mediator = container.resolve(Mediator)

    try:
        user = await mediator.handle_query(GetUserQuery(user_oid=token))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return bool(user)
