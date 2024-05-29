from typing import Any, Mapping
from domain.entities.users import User, VerificationToken
from domain.values.users import Email, Username


def convert_user_entity_to_document(user: User) -> dict:
    return {
        "oid": user.oid,
        "email": user.email.as_generic_type(),
        "username": user.username.as_generic_type(),
        "password": user.password.as_generic_type(),
        "created_at": user.created_at,
        "group_oid": user.group_id,
        "is_verified": user.is_verified,
    }


def convert_verification_token_entity_to_document(token: VerificationToken):
    return {
        "oid": token.oid,
        "token": token.token,
        "created_at": token.created_at,
        "expires_at": token.expires_at,
        "user_oid": token.user_oid,
    }


def convert_verification_token_document_to_entity(token: VerificationToken):
    return VerificationToken(
        oid=token.oid,
        token=token.token,
        created_at=token.created_at,
        expires_at=token.expires_at,
        user_oid=token.user_oid,
    )


def convert_user_document_to_entity(user_document: Mapping[str, Any]) -> User:
    return User(
        oid=user_document["oid"],
        email=Email(value=user_document["email"]),
        username=Username(value=user_document["username"]),
        password=user_document["password"],
        created_at=user_document["created_at"],
        group_id=user_document["group_oid"],
        is_verified=user_document["is_verified"],
    )
