from dataclasses import dataclass

from domain.entities.users import User, UserGroup
from domain.values.users import Email, Password, Title, Username
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import (
    GroupAlreadyExistsException,
    GroupNotFoundException,
    InvalidCredentialsException,
)


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
class UserLoginCommand(BaseCommand):
    username: str
    password: str


@dataclass(frozen=True)
class UserLoginCommandHandler(CommandHandler[UserLoginCommand, User]):
    user_repository: BaseUserRepository

    async def handle(self, command: UserLoginCommand) -> User:
        user = await self.user_repository.get_user_by_username(
            username=command.username
        )
        if user:
            if user.password.as_generic_type() == command.password:
                return user

        raise InvalidCredentialsException()


@dataclass(frozen=True)
class DeleteGroupCommand(BaseCommand):
    group_oid: str


@dataclass(frozen=True)
class DeleteGroupCommandHandler(CommandHandler[DeleteGroupCommand, UserGroup]):
    group_repository: BaseGroupRepository

    async def handle(self, command: DeleteGroupCommand) -> None:
        group = await self.group_repository.delete_group(group_oid=command.group_oid)

        if not group:
            raise GroupNotFoundException(oid=command.group_oid)

        group.delete()
        await self._mediator.publish(group.pull_events())


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

        if not group:
            raise GroupNotFoundException(oid=command.group_oid)

        new_user = await User.create(
            username=Username(value=command.username),
            email=Email(value=command.email),
            password=Password(value=command.password),
            group_id=command.group_oid,
        )

        await self.user_repository.add_user(new_user)
        await self._mediator.publish(new_user.pull_events())

        return new_user
