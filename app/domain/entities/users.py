from dataclasses import field, dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from domain.entities.base import BaseEntity
from domain.values.users import Username, Email, Password
from domain.events.users import (
    UserCreatedEvent,
    UserDeletedEvent,
    VerificationTokenCreatedEvent,
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
            UserCreatedEvent(
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
            VerificationTokenCreatedEvent(
                email=email.as_generic_type(), user_oid=user_oid, token=new_token.token
            )
        )

        return new_token
