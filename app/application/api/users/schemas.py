from collections.abc import Iterable
from datetime import datetime
from pydantic import BaseModel

from domain.entities.users import User, UserGroup


class SCreateGroupIn(BaseModel):
    title: str


class SCreateGroupOut(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, group: UserGroup) -> "SCreateGroupOut":
        return cls(oid=group.oid, title=group.title.as_generic_type())


class SCreateUserIn(BaseModel):
    email: str
    username: str
    password: str


class SCreateUserOut(BaseModel):
    oid: str
    email: str
    username: str
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "SCreateUserOut":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
        )


class SGetUser(BaseModel):
    oid: str
    email: str
    username: str
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "SGetUser":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
        )


class SGetGroup(BaseModel):
    oid: str
    title: str
    created_at: datetime
    users: Iterable[SGetUser]

    @classmethod
    def from_entity(cls, group: UserGroup) -> "SGetGroup":
        return cls(
            oid=group.oid,
            title=group.title.as_generic_type(),
            created_at=group.created_at,
            users=[SGetUser.from_entity(user) for user in group.users],
        )
