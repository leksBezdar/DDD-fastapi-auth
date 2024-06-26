from punq import Container, Scope

from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.dummy_kafka import DummyKafkaMessageBroker
from infrastructure.repositories.groups.base import BaseGroupRepository
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.memory_repository import InMemoryUserRepository
from infrastructure.repositories.groups.memory_repository import InMemoryGroupRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseGroupRepository, InMemoryGroupRepository, scope=Scope.singleton
    )
    container.register(
        BaseUserRepository, InMemoryUserRepository, scope=Scope.singleton
    )
    container.register(
        BaseMessageBroker, DummyKafkaMessageBroker, scope=Scope.singleton
    )

    return container
