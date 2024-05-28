from pytest import fixture

from punq import Container

from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.groups.base import BaseGroupRepository
from logic.mediator.base import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def group_repository(container: Container) -> BaseGroupRepository:
    return container.resolve(BaseGroupRepository)


@fixture()
def user_repository(container: Container) -> BaseUserRepository:
    return container.resolve(BaseUserRepository)
