from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import UserGroup


@dataclass(frozen=True)
class BaseGroupRepository(ABC):
    @abstractmethod
    async def check_group_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    def add_group(self, group: UserGroup) -> None: ...
