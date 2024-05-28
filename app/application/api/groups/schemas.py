from datetime import datetime
from pydantic import BaseModel

from application.api.schemas import SBaseQueryResponse
from domain.entities.groups import UserGroup


class SCreateGroupIn(BaseModel):
    title: str


class SCreateGroupOut(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, group: UserGroup) -> "SCreateGroupOut":
        return cls(oid=group.oid, title=group.title.as_generic_type())


class SGetGroup(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, group: UserGroup) -> "SGetGroup":
        return cls(
            oid=group.oid,
            title=group.title.as_generic_type(),
            created_at=group.created_at,
        )


class SGetGroupsQueryResponse(SBaseQueryResponse):
    items: list[SGetGroup]
