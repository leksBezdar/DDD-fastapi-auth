from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.users import UserGroup
from infrastructure.repositories.users.base import BaseGroupRepository
from infrastructure.repositories.users.converters import (
    convert_group_entity_to_document,
)


@dataclass(frozen=True)
class MongoDBGroupRepository(BaseGroupRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_group_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][
            self.mongo_db_collection_name
        ]

    async def check_group_exists_by_title(self, title: str) -> bool:
        collection = self._get_group_collection()

        return bool(await collection.find_one(filter={"title": title}))

    async def add_group(self, group: UserGroup) -> None:
        collection = self._get_group_collection()
        await collection.insert_one(convert_group_entity_to_document(group))
