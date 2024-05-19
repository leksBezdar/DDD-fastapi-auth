from dataclasses import dataclass

from domain.entities.users import UserGroup
from domain.values.users import Title
from infrastructure.repositories.base import BaseGroupRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import GroupAlreadyExistsException


@dataclass(frozen=True)
class CreateGroupCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateGroupCommandHandler(CommandHandler[CreateGroupCommand, UserGroup]):
    group_repository: BaseGroupRepository

    async def handle(self, command: CreateGroupCommand) -> UserGroup:
        if await self.group_repository.check_group_exists_by_title(command.title):
            raise GroupAlreadyExistsException(command.title)

        title = Title(value=command.title)
        new_group = UserGroup.create_group(title=title)
        # TODO pull events
        self.group_repository.add_group(new_group)

        return new_group
