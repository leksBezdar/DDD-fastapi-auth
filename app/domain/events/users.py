from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class UserAddedToGroupEvent(BaseEvent):
    group_oid: str
    username: str
    user_oid: str


@dataclass
class NewGroupCreated(BaseEvent):
    group_oid: str
    group_title: str
