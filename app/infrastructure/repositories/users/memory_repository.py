from dataclasses import dataclass, field
from typing import Iterable

from domain.entities.users import User
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.filters.users import GetUsersFilters


@dataclass
class InMemoryUserRepository(BaseUserRepository):
    _saved_users: list[User] = field(default_factory=list, kw_only=True)

    async def check_user_exists_by_email_and_username(
        self, email: str, username: str
    ) -> bool:
        return any(
            user.email == email or user.username == username
            for user in self._saved_users
        )

    async def add_user(self, user: User) -> None:
        self._saved_users.append(user)

    async def get_users(self, filters: GetUsersFilters) -> tuple[Iterable[User], int]:
        total_count = len(self._saved_users)
        limited_users = self._saved_users[
            filters.offset : filters.offset + filters.limit
        ]
        return limited_users, total_count

    async def get_user_by_oid(self, user_oid: str) -> User | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                return user
        return None

    async def get_user_by_username(self, username: str) -> User | None:
        for user in self._saved_users:
            if user.username == username:
                return user
        return None

    async def verify_user(self, user_oid: str) -> None:
        user = await self.get_user_by_oid(user_oid)
        user.is_verified = True

    async def delete_user(self, user_oid: str) -> User | None:
        for user in self._saved_users:
            if user.oid == user_oid:
                self._saved_users.remove(user)
                return user
        return None
