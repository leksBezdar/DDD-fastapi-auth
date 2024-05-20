from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.exceptions import SErrorMessage
from application.api.users.schemas import SCreateGroupIn, SCreateGroupOut
from domain.exceptions.base import ApplicationException
from logic.commands.users import CreateGroupCommand
from logic.init import init_container
from logic.mediator import Mediator


group_router = APIRouter()


@group_router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": SCreateGroupOut},
        status.HTTP_400_BAD_REQUEST: {"model": SErrorMessage},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_group_handler(
    group: SCreateGroupIn, container: Annotated[Container, Depends(init_container)]
):
    """Creates new user group."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        group, *_ = await mediator.handle_command(CreateGroupCommand(title=group.title))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return SCreateGroupOut.from_entity(group)
