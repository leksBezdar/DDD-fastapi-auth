import pytest


from domain.entities.users import UserGroup
from domain.values.users import Title
from infrastructure.repositories.users.base import BaseGroupRepository
from logic.commands.users import CreateGroupCommand
from logic.exceptions.users import GroupAlreadyExistsException
from logic.mediator.base import Mediator
from faker import Faker


@pytest.mark.asyncio
async def test_create_group_command_success(
    group_repository: BaseGroupRepository, mediator: Mediator, faker: Faker
):
    group: UserGroup
    group, *_ = await mediator.handle_command(CreateGroupCommand(title=faker.text(15)))
    assert await group_repository.check_group_exists_by_title(
        title=group.title.as_generic_type()
    )


@pytest.mark.asyncio
async def test_create_group_command_title_already_exists(
    group_repository: BaseGroupRepository,
    mediator: Mediator,
    faker: Faker,
):
    title_text = faker.text(15)
    group = UserGroup(title=Title(title_text))
    await group_repository.add_group(group)

    assert group in group_repository._saved_groups

    with pytest.raises(GroupAlreadyExistsException):
        await mediator.handle_command(CreateGroupCommand(title=title_text))

    assert len(group_repository._saved_groups) == 1
