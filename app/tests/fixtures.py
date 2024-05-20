from punq import Container, Scope

from infrastructure.repositories.base import BaseGroupRepository
from infrastructure.repositories.users import FakeGroupRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseGroupRepository, FakeGroupRepository, scope=Scope.singleton)

    return container
