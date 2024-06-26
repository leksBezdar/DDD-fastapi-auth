from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB settings
    mongo_db_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_group_database: str = Field(
        default="ddd-auth", alias="MONGODB_GROUP_DATABASE"
    )

    # MongoDB collections
    mongodb_group_collection: str = Field(
        default="group", alias="MONGODB_GROUP_COLLECTION"
    )
    mongodb_user_collection: str = Field(
        default="user", alias="MONGODB_USER_COLLECTION"
    )
    mongodb_verification_token_collection: str = Field(
        default="VerificationToken", alias="MONGODB_VERIFICATION_TOKEN_COLLECTION"
    )

    # Kafka topics
    verification_token_event_topic: str = Field(default="new-verification-token-topic")
    new_group_event_topic: str = Field(default="new-groups-topic")
    new_user_event_topic: str = Field(default="new-users-topic")
    group_deleted_event_topic: str = Field(default="deleted-group-topic")
    user_deleted_event_topic: str = Field(default="deleted-user-topic")

    # Kafka settings
    kafka_url: str = Field(alias="KAFKA_URL")

    # Redis settings
    redis_url: str = Field(alias="REDIS_URL")

    # Token settings
    token_secret_key: str = Field(alias="TOKEN_SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM", default="HS256")

    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(alias="REFRESH_TOKEN_EXPIRE_DAYS")
