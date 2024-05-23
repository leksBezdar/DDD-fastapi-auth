from dataclasses import dataclass

from domain.entities.users import User, UserGroup
from domain.values.users import Email, Password, Title, Username
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import GroupAlreadyExistsException, GroupNotFoundException


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

        await self.group_repository.add_group(new_group)
        await self._mediator.publish(new_group.pull_events())

        return new_group


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    email: str
    password: str
    group_oid: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    user_repository: BaseUserRepository
    group_repository: BaseGroupRepository

    async def handle(self, command: CreateUserCommand) -> User:
        group = await self.group_repository.get_group_by_oid(oid=command.group_oid)

        if not (group):
            raise GroupNotFoundException(oid=command.group_oid)

        user = User(
            username=Username(value=command.username),
            email=Email(value=command.email),
            password=Password(value=command.password),
            group_id=command.group_oid,
        )
        group.add_user(user)
        await self.user_repository.add_user(user=user)

        return user
