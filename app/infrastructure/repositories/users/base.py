from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User, UserGroup


@dataclass(frozen=True)
class BaseGroupRepository(ABC):
    @abstractmethod
    async def check_group_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def get_group_by_oid(self, oid: str) -> UserGroup | None: ...

    @abstractmethod
    async def add_group(self, group: UserGroup) -> None: ...


@dataclass(frozen=True)
class BaseUserRepository(ABC):
    @abstractmethod
    async def check_user_exists_by_username(self, username: str) -> bool: ...

    @abstractmethod
    async def add_user(self, group_oid: str, user: User) -> None: ...
