from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient, AgnosticCollection


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
