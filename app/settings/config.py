from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_group_database: str = Field(
        default="group", alias="MONGO_DB_GROUP_DATABASE"
    )
    mongodb_group_collection: str = Field(
        default="group", alias="MONGO_DB_GROUP_COLLECTION"
    )