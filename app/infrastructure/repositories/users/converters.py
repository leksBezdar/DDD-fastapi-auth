from typing import Mapping
from domain.entities.users import User, UserGroup


def convert_user_entity_to_document(user: User) -> dict:
    return {
        "oid": user.oid,
        "email": user.email.as_generic_type(),
        "username": user.username.as_generic_type(),
        "password": user.password.as_generic_type(),
        "created_at": user.created_at,
    }


def convert_user_document_to_entity(user_document: Mapping[str, any]) -> User:
    return User(
        oid=user_document["oid"],
        email=user_document["email"],
        username=user_document["username"],
        password=user_document["password"],
        created_at=user_document["created_at"],
    )


def convert_group_entity_to_document(group: UserGroup) -> dict:
    return {
        "oid": group.oid,
        "title": group.title.as_generic_type(),
        "created_at": group.created_at,
        "users": [convert_user_entity_to_document(user) for user in group.users],
    }


def convert_group_document_to_entity(group_documment: Mapping[str, any]) -> UserGroup:
    return UserGroup(
        title=group_documment["title"],
        oid=group_documment["oid"],
        created_at=group_documment["created_at"],
        users={
            convert_user_document_to_entity(user_document)
            for user_document in group_documment["users"]
        },
    )
