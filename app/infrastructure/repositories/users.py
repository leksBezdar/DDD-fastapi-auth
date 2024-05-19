from abc import ABC
from dataclasses import dataclass, field

from domain.entities.users import UserGroup


@dataclass
class FakeGroupRepository(ABC):
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

    def add_group(self, group: UserGroup) -> None:
        self._saved_groups.append(group)
