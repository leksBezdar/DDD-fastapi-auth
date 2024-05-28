from typing import Any, Mapping
from domain.entities.groups import UserGroup
from domain.values.groups import Title


def convert_group_entity_to_document(group: UserGroup) -> dict:
    return {
        "oid": group.oid,
        "title": group.title.as_generic_type(),
        "created_at": group.created_at,
    }


def convert_group_document_to_entity(group_document: Mapping[str, Any]) -> UserGroup:
    return UserGroup(
        title=Title(value=group_document["title"]),
        oid=group_document["oid"],
        created_at=group_document["created_at"],
    )
