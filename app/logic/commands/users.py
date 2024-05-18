from dataclasses import dataclass

from domain.entities.users import UserGroup
from domain.values.users import Title
from infrastructure.repositories.users import BaseGroupRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import GroupAlreadyExistsException


@dataclass(frozen=False)
class CreateGroupCommand(BaseCommand):
    title: str


class CreateGroupCommandHandler(CommandHandler[CreateGroupCommand]):
    group_repository: BaseGroupRepository

    async def handle(self, command: CreateGroupCommand) -> UserGroup:
        if self.group_repository.check_group_exists_by_title(command.title):
            raise GroupAlreadyExistsException(command.title)

        title = Title(value=command.title)
        # TODO pull events
        return UserGroup.create_group(title=title)
