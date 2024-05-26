from dataclasses import field, dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username, Email, Password
from domain.events.users import (
    GroupDeletedEvent,
    NewGroupCreatedEvent,
    NewUserCreatedEvent,
)


@dataclass(eq=False)
class User(BaseEntity):
    email: Email
    username: Username
    password: Password
    group_id: str
    is_verified: bool = field(default=False, kw_only=True)

    @classmethod
    async def create(
        cls, username: Username, password: Password, email: Email, group_id: str
    ) -> "User":
        new_user = cls(
            email=email, username=username, password=password, group_id=group_id
        )
        new_user.register_event(
            NewUserCreatedEvent(
                username=new_user.username.as_generic_type(),
                email=new_user.email.as_generic_type(),
                user_oid=new_user.oid,
                group_oid=group_id,
            )
        )

        return new_user


@dataclass(eq=False)
class VerificationToken(BaseEntity):
    token: str
    user_oid: str
    expires_at: datetime


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    is_deleted: bool = field(default=False, kw_only=True)

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

    def delete(self):
        self.is_deleted = True
        self.register_event(
            GroupDeletedEvent(
                group_oid=self.oid, group_title=self.title.as_generic_type()
            )
        )
