from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.schemas import SErrorMessage
from application.api.users.filters import GetUsersFilters
from application.api.users.schemas import (
    SCreateUserIn,
    SCreateUserOut,
    SGetUser,
    SGetUsersQueryResponse,
    SLoginIn,
    SLoginOut,
)
from domain.exceptions.base import ApplicationException
from logic.commands.users import (
    CreateUserCommand,
    CreateVerificationTokenCommand,
    DeleteUserCommand,
    UserLoginCommand,
    VerifyUserCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.users import (
    GetUsersQuery,
)


user_router = APIRouter()


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


@user_router.delete(
    "/{user_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage}},
)
async def delete_user(
    user_oid: str,
    container: Annotated[Container, Depends(init_container)],
) -> None:
    """Delete user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(DeleteUserCommand(user_oid=user_oid))
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


@user_router.post(
    "/{user_oid}/verify/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage}},
)
async def send_verification_request(
    user_oid: str,
    container: Annotated[Container, Depends(init_container)],
):
    """Send verification request to user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(CreateVerificationTokenCommand(user_oid=user_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@user_router.get(
    "/{user_oid}/verify/{token}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage}},
)
async def verify_user(
    user_oid: str,
    token: str,
    container: Annotated[Container, Depends(init_container)],
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(VerifyUserCommand(user_oid=user_oid, token=token))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
