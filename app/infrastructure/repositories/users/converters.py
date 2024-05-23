from typing import Any, Mapping
from domain.entities.users import User, UserGroup
from domain.values.users import Email, Password, Title, Username


def convert_user_entity_to_document(user: User) -> dict:
    return {
        "oid": user.oid,
        "email": user.email.as_generic_type(),
        "username": user.username.as_generic_type(),
        "password": user.password.as_generic_type(),
        "created_at": user.created_at,
        "group_oid": user.group_id,
    }


def convert_group_entity_to_document(group: UserGroup) -> dict:
    return {
        "oid": group.oid,
        "title": group.title.as_generic_type(),
        "created_at": group.created_at,
    }


def convert_user_document_to_entity(user_document: Mapping[str, Any]) -> User:
    return User(
        oid=user_document["oid"],
        email=Email(value=user_document["email"]),
        username=Username(value=user_document["username"]),
        password=Password(value=user_document["password"]),
        created_at=user_document["created_at"],
        group_id=user_document["group_oid"],
    )


def convert_group_document_to_entity(group_documment: Mapping[str, Any]) -> UserGroup:
    return UserGroup(
        title=Title(value=group_documment["title"]),
        oid=group_documment["oid"],
        created_at=group_documment["created_at"],
    )
