from pytest import fixture

from punq import Container

from infrastructure.repositories.base import BaseGroupRepository
from logic.mediator import Mediator
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
