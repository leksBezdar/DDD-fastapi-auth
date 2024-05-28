from dataclasses import dataclass
from typing import ClassVar
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass
class UserCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New User Added To Group"

    username: str
    user_oid: str
    group_oid: str
    email: str
    token: str = str(uuid4())


@dataclass
class GroupCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Group Created"

    group_oid: str
    group_title: str


@dataclass
class VerificationTokenCreatedEvent(BaseEvent):
    title: ClassVar[str] = "Verification token created"

    user_oid: str
    email: str
    token: str


@dataclass
class GroupDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Group was deleted"

    group_oid: str
    group_title: str


@dataclass
class UserDeletedEvent(BaseEvent):
    title: ClassVar[str] = "User was deleted"

    user_oid: str
    username: str
    email: str
    group_oid: str
