from functools import lru_cache
from punq import Container, Scope

from infrastructure.repositories.base import BaseGroupRepository
from infrastructure.repositories.users import FakeGroupRepository
from logic.commands.users import CreateGroupCommand, CreateGroupCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(BaseGroupRepository, FakeGroupRepository, scope=Scope.singleton)
    container.register(CreateGroupCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateGroupCommand,
            [container.resolve(CreateGroupCommandHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
