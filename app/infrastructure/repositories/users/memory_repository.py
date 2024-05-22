from dataclasses import dataclass, field

from domain.entities.users import UserGroup
from infrastructure.repositories.users.base import BaseGroupRepository


@dataclass
class InMemoryGroupRepository(BaseGroupRepository):
    _saved_groups: list[UserGroup] = field(default_factory=list, kw_only=True)

    async def check_group_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    group
                    for group in self._saved_groups
                    if group.title.as_generic_type() == title
                )
            )
        except StopIteration:
            return False

    async def get_group_by_oid(self, oid: str) -> UserGroup | None:
        try:
            return next(group for group in self._saved_groups if group.oid == oid)
        except StopIteration:
            return None

    async def add_group(self, group: UserGroup) -> None:
        self._saved_groups.append(group)
