from abc import ABC, abstractmethod
from collections.abc import Iterable

from domain.entities.users import User, UserGroup
from infrastructure.repositories.users.filters.users import (
    GetGroupsFilters,
    GetUsersFilters,
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


class BaseUserRepository(ABC):
    @abstractmethod
    async def check_user_exists_by_email_and_username(
        self, email: str, username: str
    ) -> bool: ...

    @abstractmethod
    async def add_user(self, user: User) -> None: ...

    @abstractmethod
    async def get_users(
        self, group_oid: str, filters: GetUsersFilters
    ) -> tuple[Iterable[User], int]: ...

    @abstractmethod
    async def get_user_by_oid(self, user_oid: str) -> User | None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def delete_user(self, user_oid: str) -> User | None: ...
