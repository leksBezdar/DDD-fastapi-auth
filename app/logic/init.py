from functools import lru_cache
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from infrastructure.repositories.users.mongo import (
    MongoDBGroupRepository,
    MongoDBUserRepository,
)
from logic.commands.users import (
    CreateGroupCommand,
    CreateGroupCommandHandler,
    CreateUserCommand,
    CreateUserCommandHandler,
)
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.users import (
    GetGroupQuery,
    GetGroupQueryHandler,
    GetUserQuery,
    GetUserQueryHandler,
)
from settings.config import Settings


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    settings: Settings = container.resolve(Settings)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            settings.mongo_db_connection_uri, serverSelectionTimeoutMS=3000
        )

    container.register(
        AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton
    )
    client = container.resolve(AsyncIOMotorClient)

    def init_group_mongodb_repository() -> BaseGroupRepository:
        return MongoDBGroupRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongodb_group_database,
            mongo_db_collection_name=settings.mongodb_group_collection,
        )

    def init_user_mongodb_repository() -> BaseUserRepository:
        return MongoDBUserRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongodb_group_database,
            mongo_db_collection_name=settings.mongodb_user_collection,
        )

    container.register(
        BaseGroupRepository,
        factory=init_group_mongodb_repository,
        scope=Scope.singleton,
    )
    container.register(
        BaseUserRepository, factory=init_user_mongodb_repository, scope=Scope.singleton
    )

    # Command handlers
    container.register(CreateGroupCommandHandler)
    container.register(CreateUserCommandHandler)

    # Query Handlers
    container.register(GetGroupQueryHandler)
    container.register(GetUserQueryHandler)

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_handler = CreateGroupCommandHandler(
            _mediator=mediator, group_repository=container.resolve(BaseGroupRepository)
        )
        create_message_handler = CreateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            group_repository=container.resolve(BaseGroupRepository),
        )

        mediator.register_command(
            CreateGroupCommand,
            [create_chat_handler],
        )
        mediator.register_command(
            CreateUserCommand,
            [create_message_handler],
        )
        mediator.register_query(
            GetGroupQuery,
            container.resolve(GetGroupQueryHandler),
        )
        mediator.register_query(
            GetUserQuery,
            container.resolve(GetUserQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
