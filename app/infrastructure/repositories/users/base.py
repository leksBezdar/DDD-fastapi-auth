from abc import ABC, abstractmethod
from collections.abc import Iterable

from domain.entities.users import User, VerificationToken
from infrastructure.repositories.users.filters.users import (
    GetUsersFilters,
)


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
    async def verify_user(self, user_oid: str) -> None: ...

    @abstractmethod
    async def check_password_is_valid(
        self, password: str, hashed_password: str
    ) -> bool: ...

    @abstractmethod
    async def delete_user(self, user_oid: str) -> User | None: ...


class BaseVerificationTokenRepository(ABC):
    @abstractmethod
    async def add_token(self, token: VerificationToken) -> None: ...

    @abstractmethod
    async def check_token_exists(self, token: str) -> bool: ...
