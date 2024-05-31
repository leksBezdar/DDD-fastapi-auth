from dataclasses import dataclass, field
from typing import Iterable

from domain.entities.groups import UserGroup
from infrastructure.repositories.groups.base import BaseGroupRepository
from infrastructure.repositories.groups.filters.groups import GetGroupsFilters


@dataclass
class InMemoryGroupRepository(BaseGroupRepository):
    _saved_groups: list[UserGroup] = field(default_factory=list, kw_only=True)

    async def check_group_exists_by_title(self, title: str) -> bool:
        return any(
            group.title.as_generic_type() == title for group in self._saved_groups
        )

    async def get_group_by_oid(self, group_oid: str) -> UserGroup | None:
        for group in self._saved_groups:
            if group.oid == group_oid:
                return group
        return None

    async def add_group(self, group: UserGroup) -> None:
        self._saved_groups.append(group)

    async def get_groups(
        self, filters: GetGroupsFilters
    ) -> tuple[Iterable[UserGroup], int]:
        raise Exception(self._saved_groups)
        filtered_groups = [
            group for group in self._saved_groups if not group.is_deleted
        ]
        total_count = len(filtered_groups)
        limited_groups = filtered_groups[
            filters.offset : filters.offset + filters.limit
        ]
        return limited_groups, total_count

    async def delete_group(self, group_oid: str) -> UserGroup | None:
        for group in self._saved_groups:
            if group.oid == group_oid:
                self._saved_groups.remove(group)
                return group
        return None
