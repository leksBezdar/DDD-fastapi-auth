from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.exceptions import SErrorMessage
from application.api.users.schemas import (
    SCreateGroupIn,
    SCreateGroupOut,
    SCreateUserIn,
    SCreateUserOut,
)
from domain.exceptions.base import ApplicationException
from logic.commands.users import CreateGroupCommand, CreateUserCommand
from logic.init import init_container
from logic.mediator import Mediator


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
async def create_group_handler(
    group: SCreateGroupIn, container: Annotated[Container, Depends(init_container)]
) -> SCreateGroupOut:
    """Creates new user group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        group, *_ = await mediator.handle_command(CreateGroupCommand(title=group.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateGroupOut.from_entity(group)


@user_router.post(
    "/{group_oid}/users",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": SCreateUserOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
)
async def create_user_handler(
    group_oid: str,
    user: SCreateUserIn,
    container: Annotated[Container, Depends(init_container)],
) -> SCreateUserOut:
    """Creates new user."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(
                email=user.email,
                username=user.username,
                password=user.password,
                group_oid=group_oid,
            )
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateUserOut.from_entity(user)
