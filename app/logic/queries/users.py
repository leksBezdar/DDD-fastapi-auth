from dataclasses import dataclass
from typing import Generic

from domain.entities.users import UserGroup
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from logic.exceptions.users import GroupNotFoundException
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetGroupQuery(BaseQuery):
    group_oid: str


@dataclass(frozen=True)
class GetGroupQueryHandler(BaseQueryHandler, Generic[QR, QT]):
    group_repository: BaseGroupRepository
    users_repository: BaseUserRepository  # TODO pull users separately

    async def handle(self, query: GetGroupQuery) -> UserGroup:
        group = await self.group_repository.get_group_by_oid(oid=query.group_oid)

        if not group:
            raise GroupNotFoundException(oid=query.group_oid)

        return group
