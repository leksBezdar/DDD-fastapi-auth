from pydantic import BaseModel

from domain.entities.users import UserGroup


class SCreateGroupIn(BaseModel):
    title: str


class SCreateGroupOut(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, group: UserGroup) -> "SCreateGroupOut":
        return SCreateGroupOut(oid=group.oid, title=group.title.as_generic_type())
