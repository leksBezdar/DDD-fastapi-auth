import pytest

from domain.entities.users import UserGroup
from infrastructure.repositories.base import BaseGroupRepository
from logic.commands.users import CreateGroupCommand
from logic.mediator import Mediator
from faker import Faker


@pytest.mark.asyncio
async def test_create_group_command_success(
    group_repository: BaseGroupRepository, mediator: Mediator, faker: Faker
):
    # TODO: Use faker for data generation
    group: UserGroup = (
        await mediator.handle_command(CreateGroupCommand(title=faker.text(15)))
    )[0]
    assert await group_repository.check_group_exists_by_title(
        title=group.title.as_generic_type()
    )
