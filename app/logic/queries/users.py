from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.users import User, UserGroup
from infrastructure.repositories.users.base import (
    BaseGroupRepository,
    BaseUserRepository,
)
from infrastructure.repositories.users.filters.users import (
    GetGroupsFilters,
    GetUsersFilters,
)
from logic.exceptions.users import GroupNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetGroupQuery(BaseQuery):
    group_oid: str


@dataclass(frozen=True)
class GetGroupsQuery(BaseQuery):
    filters: GetGroupsFilters


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
        return await self.users_repository.get_user(user_oid=query.user_oid)


@dataclass(frozen=True)
class GetGroupQueryHandler(BaseQueryHandler):
    group_repository: BaseGroupRepository

    async def handle(self, query: GetGroupQuery) -> UserGroup:
        group = await self.group_repository.get_group_by_oid(oid=query.group_oid)

        if not group:
            raise GroupNotFoundException(oid=query.group_oid)

        return group


@dataclass(frozen=True)
class GetGroupsQueryHandler(BaseQueryHandler):
    groups_repository: BaseGroupRepository

    async def handle(self, query: GetUsersQuery) -> Iterable[User]:
        return await self.groups_repository.get_groups(filters=query.filters)


@dataclass(frozen=True)
class GetUsersQueryHandler(BaseQueryHandler):
    users_repository: BaseUserRepository

    async def handle(self, query: GetUsersQuery) -> Iterable[User]:
        return await self.users_repository.get_users(
            group_oid=query.group_oid, filters=query.filters
        )
