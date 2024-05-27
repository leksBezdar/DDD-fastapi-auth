from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_group_database: str = Field(
        default="ddd-auth", alias="MONGODB_GROUP_DATABASE"
    )
    mongodb_group_collection: str = Field(
        default="group", alias="MONGODB_GROUP_COLLECTION"
    )
    mongodb_user_collection: str = Field(
        default="user", alias="MONGODB_USER_COLLECTION"
    )
    mongodb_verification_token_collection: str = Field(
        default="verification_token", alias="MONGODB_VERIFICATION_TOKEN_COLLECTION"
    )
    new_group_event_topic: str = Field(default="new-groups-topic")
    new_user_event_topic: str = Field(default="new-users-topic")
    group_deleted_event_topic: str = Field(default="deleted-group-topic")
    user_deleted_event_topic: str = Field(default="deleted-user-topic")

    kafka_url: str = Field(alias="KAFKA_URL")
