from domain.entities.users import User, UserGroup


def convert_user_to_document(user: User) -> dict:
    return {
        "oid": user.oid,
        "email": user.email.as_generic_type(),
        "username": user.username.as_generic_type(),
        "password": user.password.as_generic_type(),
        "created_at": user.created_at,
    }


def convert_group_entity_to_document(group: UserGroup) -> dict:
    return {
        "oid": group.oid,
        "title": group.title.as_generic_type(),
        "created_at": group.created_at,
        "users": [convert_user_to_document(user) for user in group.users],
    }
