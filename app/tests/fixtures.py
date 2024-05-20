from punq import Container, Scope

from infrastructure.repositories.users.base import BaseGroupRepository
from infrastructure.repositories.users.fake_repository import FakeGroupRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseGroupRepository, FakeGroupRepository, scope=Scope.singleton)

    return container
