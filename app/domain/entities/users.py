from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username, Email, Password
from domain.events.users import NewGroupCreated, UserAddedToGroupEvent


@dataclass(eq=False)
class User(BaseEntity):
    email: Email
    username: Username
    password: Password


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    users: set[User] = field(default_factory=set, kw_only=True)

    def add_user(self, user: User):
        self.users.add(user)
        self.register_event(
            UserAddedToGroupEvent(
                username=user.username.as_generic_type(),
                user_oid=user.oid,
                group_oid=self.oid,
            )
        )

    @classmethod
    def create_group(cls, title: Title) -> "UserGroup":
        new_group = cls(title=title)
        new_group.register_event(
            NewGroupCreated(group_oid=cls.oid, group_title=title.as_generic_type())
        )
