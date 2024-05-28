from datetime import datetime
from pydantic import BaseModel, EmailStr

from application.api.schemas import SBaseQueryResponse
from domain.entities.users import User


class SCreateUserIn(BaseModel):
    email: EmailStr
    username: str
    password: str


class SCreateUserOut(BaseModel):
    oid: str
    email: str
    username: str
    created_at: datetime
    is_verified: bool

    @classmethod
    def from_entity(cls, user: User) -> "SCreateUserOut":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
        )


class SLoginIn(BaseModel):
    username: str
    password: str


class SLoginOut(BaseModel):
    oid: str
    email: EmailStr
    username: str
    created_at: datetime
    is_verified: bool
    group_oid: str

    @classmethod
    def from_entity(cls, user: User) -> "SLoginOut":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
            group_oid=user.group_id,
        )


class SGetUser(BaseModel):
    oid: str
    email: EmailStr
    username: str
    created_at: datetime
    is_verified: bool
    group_oid: str

    @classmethod
    def from_entity(cls, user: User) -> "SGetUser":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            created_at=user.created_at,
            is_verified=user.is_verified,
            group_oid=user.group_id,
        )


class SGetUsersQueryResponse(SBaseQueryResponse):
    items: list[SGetUser]
