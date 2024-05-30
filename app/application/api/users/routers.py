from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.schemas import SErrorMessage
from application.api.users.schemas import (
    SCreateUserIn,
    SCreateUserOut,
    SGetUser,
    SLoginIn,
    SLoginOut,
)
from domain.exceptions.base import ApplicationException
from domain.exceptions.users import (
    InvalidEmail,
    InvalidPasswordLength,
    InvalidUsernameLength,
)
from logic.commands.users import (
    CreateUserCommand,
    CreateVerificationTokenCommand,
    DeleteUserCommand,
    UserLoginCommand,
    VerifyUserCommand,
)
from logic.exceptions.users import (
    InvalidCredentialsException,
    TokenNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.users import (
    GetUserQuery,
)


user_router = APIRouter()


@user_router.post(
    "/{group_oid}/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateUserOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_409_CONFLICT: {"model": UserAlreadyExistsException},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": InvalidEmail | InvalidUsernameLength | InvalidPasswordLength
        },
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
        raise HTTPException(status_code=e.status_code, detail=e.message)

    return SCreateUserOut.from_entity(user)


@user_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SLoginOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsException},
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
    "/{user_oid}/verify/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
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
    "/{user_oid}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SGetUser},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
)
async def get_user(
    user_oid: str,
    container: Annotated[Container, Depends(init_container)],
):
    """Get user user info."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        user = await mediator.handle_query(GetUserQuery(user_oid=user_oid))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SGetUser.from_entity(user)


@user_router.get(
    "/{user_oid}/verify/{token}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {
            "model": UserNotFoundException | TokenNotFoundException
        },
    },
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


@user_router.delete(
    "/{user_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
        status.HTTP_404_NOT_FOUND: {"model": UserNotFoundException},
    },
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
