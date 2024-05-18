from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.users import UserGroup


@dataclass(frozen=True)
class BaseGroupRepository(ABC):
    @abstractmethod
    def check_group_exists_by_title(self, title: str) -> bool: ...


@dataclass
class FakeGroupRepository(ABC):
    _saved_groups: list[UserGroup] = field(default_factory=list, kw_only=True)

    def check_group_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(group for group in self._saved_groups if group.title == title)
            )
        except StopIteration:
            return False
