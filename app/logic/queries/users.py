from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.users import User
from infrastructure.repositories.users.base import (
    BaseUserRepository,
)
from infrastructure.repositories.users.filters.users import (
    GetUsersFilters,
)
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetUsersQuery(BaseQuery):
    group_oid: str
    filters: GetUsersFilters


@dataclass(frozen=True)
class GetUserQuery(BaseQuery):
    user_oid: str


@dataclass(frozen=True)
class GetUserQueryHandler(BaseQueryHandler):
    users_repository: BaseUserRepository

    async def handle(self, query: GetUserQuery) -> User | None:
        return await self.users_repository.get_user_by_oid(user_oid=query.user_oid)


@dataclass(frozen=True)
class GetUsersQueryHandler(BaseQueryHandler):
    users_repository: BaseUserRepository

    async def handle(self, query: GetUsersQuery) -> Iterable[User]:
        return await self.users_repository.get_users(
            group_oid=query.group_oid, filters=query.filters
        )
