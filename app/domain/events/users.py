from dataclasses import dataclass
from typing import ClassVar
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass
class NewUserCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New User Added To Group"

    username: str
    user_oid: str
    group_oid: str
    email: str
    token: str = str(uuid4())


@dataclass
class NewGroupCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Group Created"

    group_oid: str
    group_title: str


@dataclass
class GroupDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Group was deleted"

    group_oid: str
    group_title: str
