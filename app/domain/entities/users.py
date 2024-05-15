from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username


@dataclass(eq=False)
class User(BaseEntity):
    username: Username


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    users: set[User] = field(default_factory=set, kw_only=True)

    def add_user(self, user: User):
        self.users.add(user)
