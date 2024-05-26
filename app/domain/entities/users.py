from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username, Email, Password
from domain.events.users import NewGroupCreatedEvent, NewUserCreatedEvent


@dataclass(eq=False)
class User(BaseEntity):
    email: Email
    username: Username
    password: Password
    group_id: str
    is_verified: bool = False

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
