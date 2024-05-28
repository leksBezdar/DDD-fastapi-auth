from dataclasses import field, dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from domain.entities.base import BaseEntity
from domain.values.users import Title, Username, Email, Password
from domain.events.users import (
    GroupDeletedEvent,
    NewGroupCreatedEvent,
    NewUserCreatedEvent,
    UserDeletedEvent,
    VerificationTokenSentEvent,
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

    def delete(self) -> None:
        self.register_event(
            UserDeletedEvent(
                user_oid=self.oid,
                username=self.username.as_generic_type(),
                email=self.email.as_generic_type(),
                group_oid=self.group_id,
            )
        )


@dataclass(eq=False)
class VerificationToken(BaseEntity):
    user_oid: str
    expires_at: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(hours=1),
        kw_only=True,
    )
    token: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )

    @classmethod
    def create(cls, email: Email, user_oid: str) -> "VerificationToken":
        new_token = cls(user_oid=user_oid)
        new_token.register_event(
            VerificationTokenSentEvent(
                email=email.as_generic_type(), user_oid=user_oid, token=new_token.token
            )
        )

        return new_token


@dataclass(eq=False)
class UserGroup(BaseEntity):
    title: Title
    is_deleted: bool = field(default=False, kw_only=True)

    @classmethod
    def create(cls, title: Title) -> "UserGroup":
        new_group = cls(title=title)
        new_group.register_event(
            NewGroupCreatedEvent(
                group_title=new_group.title.as_generic_type(),
                group_oid=new_group.oid,
            )
        )

        return new_group

    def delete(self) -> None:
        self.is_deleted = True
        self.register_event(
            GroupDeletedEvent(
                group_oid=self.oid, group_title=self.title.as_generic_type()
            )
        )
