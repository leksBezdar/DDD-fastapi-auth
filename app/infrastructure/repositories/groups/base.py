from abc import ABC, abstractmethod
from collections.abc import Iterable

from domain.entities.groups import UserGroup

from infrastructure.repositories.groups.filters.groups import (
    GetGroupsFilters,
)


class BaseGroupRepository(ABC):
    @abstractmethod
    async def check_group_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_group_by_oid(self, group_oid: str) -> UserGroup | None: ...

    @abstractmethod
    async def add_group(self, group: UserGroup) -> None: ...

    @abstractmethod
    async def get_groups(
        self, filters: GetGroupsFilters
    ) -> tuple[Iterable[UserGroup], int]: ...

    @abstractmethod
    async def delete_group(self, group_oid: str) -> UserGroup | None: ...
