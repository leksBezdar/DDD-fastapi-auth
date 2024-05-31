from collections.abc import Iterable
from dataclasses import dataclass


from domain.entities.groups import UserGroup
from infrastructure.repositories.common.base_repository import BaseMongoDBRepository
from infrastructure.repositories.groups.base import (
    BaseGroupRepository,
)
from infrastructure.repositories.groups.converters import (
    convert_group_document_to_entity,
    convert_group_entity_to_document,
)
from infrastructure.repositories.groups.filters.groups import (
    GetGroupsFilters,
)


@dataclass(frozen=True)
class MongoDBGroupRepository(BaseGroupRepository, BaseMongoDBRepository):
    async def get_group_by_oid(self, group_oid: str) -> UserGroup | None:
        group_document = await self._collection.find_one(filter={"oid": group_oid})

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
        count = await self._collection.count_documents({})

        return groups, count

    async def delete_group(self, group_oid: str) -> UserGroup | None:
        group = await self._collection.find_one_and_delete(filter={"oid": group_oid})
        if group:
            return convert_group_document_to_entity(group_document=group)
