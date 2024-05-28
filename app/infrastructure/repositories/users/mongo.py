from abc import ABC
from collections.abc import Iterable
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection

from domain.entities.users import User, UserGroup, VerificationToken
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
    BaseVerificationTokenRepository,
)
from infrastructure.repositories.users.converters import (
    convert_group_document_to_entity,
    convert_group_entity_to_document,
    convert_user_document_to_entity,
    convert_user_entity_to_document,
    convert_verification_token_entity_to_document,
)
from infrastructure.repositories.users.filters.users import (
    GetGroupsFilters,
    GetUsersFilters,
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

    async def get_groups(
        self, filters: GetGroupsFilters
    ) -> tuple[Iterable[UserGroup], int]:
        cursor = self._collection.find().skip(filters.offset).limit(filters.limit)

        groups = [
            convert_group_document_to_entity(group_document=group_document)
            async for group_document in cursor
        ]
        count = await self._collection.count_documents(filter={})

        return groups, count

    async def delete_group(self, group_oid: str) -> UserGroup | None:
        group = await self._collection.find_one_and_delete(filter={"oid": group_oid})
        if group:
            return convert_group_document_to_entity(group_document=group)


@dataclass(frozen=True)
class MongoDBUserRepository(BaseUserRepository, BaseMongoDBRepository):
    async def check_user_exists_by_email_and_username(
        self, email: str, username: str
    ) -> bool:
        filter_query = {"$or": [{"email": email}, {"username": username}]}
        return bool(await self._collection.find_one(filter=filter_query))

    async def add_user(self, user: User) -> None:
        await self._collection.insert_one(convert_user_entity_to_document(user))

    async def get_user_by_oid(self, user_oid: str) -> User | None:
        user = await self._collection.find_one(filter={"oid": user_oid})
        if user:
            return convert_user_document_to_entity(user_document=user)

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self._collection.find_one(filter={"username": username})
        if user:
            return convert_user_document_to_entity(user_document=user)

    async def get_users(
        self, group_oid: str, filters: GetUsersFilters
    ) -> tuple[Iterable[User], int]:
        find_conditions = {"group_oid": group_oid}
        cursor = (
            self._collection.find(find_conditions)
            .skip(filters.offset)
            .limit(filters.limit)
        )

        users = [
            convert_user_document_to_entity(user_document=user_document)
            async for user_document in cursor
        ]
        count = await self._collection.count_documents(filter=find_conditions)

        return users, count

    async def verify_user(self, user_oid: str) -> None:
        await self._collection.update_one(
            filter={"oid": user_oid}, update={"$set": {"is_verified": True}}
        )

    async def delete_user(self, user_oid: str) -> User | None:
        user = await self._collection.find_one_and_delete(filter={"oid": user_oid})
        if user:
            return convert_user_document_to_entity(user_document=user)


@dataclass(frozen=True)
class MongoDBVerificationTokenRepository(
    BaseVerificationTokenRepository, BaseMongoDBRepository
):
    async def add_token(self, token: VerificationToken) -> None:
        await self._collection.insert_one(
            convert_verification_token_entity_to_document(token=token)
        )

    async def check_token_exists(self, token: str) -> bool:
        return bool(await self._collection.find_one_and_delete(filter={"token": token}))
