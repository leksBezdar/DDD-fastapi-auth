from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewUserCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New User Added To Group"

    username: str
    user_oid: str
    group_oid: str


@dataclass
class NewGroupCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Group Created"

    group_oid: str
    group_title: str
