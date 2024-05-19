from infrastructure.repositories.base import BaseGroupRepository
from logic.commands.users import CreateGroupCommand, CreateGroupCommandHandler
from logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    group_repository: BaseGroupRepository,
):
    mediator.register_command(
        CreateGroupCommand,
        [CreateGroupCommandHandler(group_repository=group_repository)],
    )

    return mediator
