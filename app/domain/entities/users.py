from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username, Email, Password
from domain.events.users import NewGroupCreatedEvent, NewUserCreatedEvent


@dataclass(eq=False)
class User(BaseEntity):
    email: Email
    username: Username
    password: Password
    group_id: str


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    users: set[User] = field(default_factory=set, kw_only=True)

    def add_user(self, user: User):
        self.users.add(user)
        self.register_event(
            NewUserCreatedEvent(
                username=user.username.as_generic_type(),
                user_oid=user.oid,
                group_oid=self.oid,
            )
        )

    @classmethod
    def create_group(cls, title: Title) -> "UserGroup":
        new_group = cls(title=title)
        new_group.register_event(
            NewGroupCreatedEvent(
                group_title=new_group.title.as_generic_type(),
                group_oid=new_group.oid,
            )
        )

        return new_group
