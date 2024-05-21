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

    @classmethod
    def from_entity(cls, user: User) -> "SCreateUserOut":
        return cls(
            oid=user.oid,
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
        )
