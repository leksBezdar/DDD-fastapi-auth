from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class UserAddedToGroupEvent(BaseEvent):
    username: str
    user_oid: str
    group_oid: str


@dataclass
class NewGroupCreated(BaseEvent):
    group_oid: str
    group_title: str
