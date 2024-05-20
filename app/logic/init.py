from functools import lru_cache
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from infrastructure.repositories.users.base import BaseGroupRepository
from infrastructure.repositories.users.mongo import MongoDBGroupRepository
from logic.commands.users import CreateGroupCommand, CreateGroupCommandHandler
from logic.mediator import Mediator
from settings.config import Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateGroupCommandHandler)
    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateGroupCommand,
            [container.resolve(CreateGroupCommandHandler)],
        )

        return mediator

    def init_group_mongodb_repository():
        settings: Settings = container.resolve(Settings)
        client = AsyncIOMotorClient(
            settings.mongo_db_connection_uri, serverSelectionTimeoutMS=3000
        )

        return MongoDBGroupRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongodb_group_database,
            mongo_db_collection_name=settings.mongodb_group_collection,
        )

    container.register(
        BaseGroupRepository,
        factory=init_group_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(Mediator, factory=init_mediator)
    return container
