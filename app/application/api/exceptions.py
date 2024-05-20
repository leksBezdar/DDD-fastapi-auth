from pydantic import BaseModel


class SErrorMessage(BaseModel):
    error: str
