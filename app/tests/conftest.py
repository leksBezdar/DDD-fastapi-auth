from pytest import fixture

from infrastructure.repositories.base import BaseGroupRepository
from infrastructure.repositories.users import FakeGroupRepository

from logic.init import init_mediator
from logic.mediator import Mediator


@fixture(scope="function")
def group_repository() -> FakeGroupRepository:
    return FakeGroupRepository()


@fixture(scope="function")
def mediator(group_repository: BaseGroupRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, group_repository=group_repository)

    return mediator
