from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class GroupCreatedEvent(BaseEvent):
    title: ClassVar[str] = "New Group Created"

    group_oid: str
    group_title: str


@dataclass
class GroupDeletedEvent(BaseEvent):
    title: ClassVar[str] = "Group was deleted"

    group_oid: str
    group_title: str
