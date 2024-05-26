from functools import lru_cache
from uuid import uuid4
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from domain.events.users import NewGroupCreatedEvent, NewUserCreatedEvent
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
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
from logic.events.users import NewGroupCreatedEventHandler, NewUserCreatedEventHandler
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
from logic.queries.users import (
    GetGroupQuery,
    GetGroupQueryHandler,
    GetGroupsQuery,
    GetGroupsQueryHandler,
    GetUserQuery,
    GetUserQueryHandler,
    GetUsersQuery,
    GetUsersQueryHandler,
)
from settings.config import Settings


@lru_cache(1)
def init_container() -> Container:
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
    container.register(GetUsersQueryHandler)
    container.register(GetGroupsQueryHandler)
    container.register(GetUserQueryHandler)

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.kafka_url,
                group_id=f"{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    # Message Broker
    container.register(
        BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton
    )

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Command Handlers
        create_group_handler = CreateGroupCommandHandler(
            _mediator=mediator, group_repository=container.resolve(BaseGroupRepository)
        )
        create_user_handler = CreateUserCommandHandler(
            _mediator=mediator,
            user_repository=container.resolve(BaseUserRepository),
            group_repository=container.resolve(BaseGroupRepository),
        )

        mediator.register_command(
            CreateGroupCommand,
            [create_group_handler],
        )
        mediator.register_command(
            CreateUserCommand,
            [create_user_handler],
        )

        # Event Handlers
        new_group_created_event_handler = NewGroupCreatedEventHandler(
            broker_topic=settings.new_group_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )
        new_user_created_event_handler = NewUserCreatedEventHandler(
            broker_topic=settings.new_user_event_topic,
            message_broker=container.resolve(BaseMessageBroker),
        )
        mediator.register_event(
            NewGroupCreatedEvent,
            [new_group_created_event_handler],
        )
        mediator.register_event(
            NewUserCreatedEvent,
            [new_user_created_event_handler],
        )

        # Query Handlers
        mediator.register_query(
            GetGroupQuery,
            container.resolve(GetGroupQueryHandler),
        )
        mediator.register_query(
            GetGroupsQuery,
            container.resolve(GetGroupsQueryHandler),
        )
        mediator.register_query(
            GetUsersQuery,
            container.resolve(GetUsersQueryHandler),
        )
        mediator.register_query(
            GetUserQuery,
            container.resolve(GetUserQueryHandler),
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
