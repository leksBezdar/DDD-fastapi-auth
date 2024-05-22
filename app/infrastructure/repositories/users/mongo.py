from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection

from domain.entities.users import User, UserGroup
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from infrastructure.repositories.users.converters import (
    convert_group_document_to_entity,
    convert_group_entity_to_document,
    convert_user_entity_to_document,
)


@dataclass(frozen=True)
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self) -> AgnosticCollection:
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]


@dataclass(frozen=True)
class MongoDBGroupRepository(BaseGroupRepository, BaseMongoDBRepository):
    async def get_group_by_oid(self, oid: str) -> UserGroup | None:
        group_document = await self._collection.find_one(filter={"oid": oid})

        if not group_document:
            return None

        return convert_group_document_to_entity(group_document)

    async def check_group_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def add_group(self, group: UserGroup) -> None:
        await self._collection.insert_one(convert_group_entity_to_document(group))


@dataclass(frozen=True)
class MongoDBUserRepository(BaseUserRepository, BaseMongoDBRepository):
    async def check_user_exists_by_username(self, username: str) -> bool:
        return bool(await self._collection.find_one(filter={"username": username}))

    async def add_user(self, group_oid: str, user: User) -> None:
        await self._collection.update_one(
            filter={"oid": group_oid},
            update={
                "$push": {"users": convert_user_entity_to_document(user=user)},
            },
        )
