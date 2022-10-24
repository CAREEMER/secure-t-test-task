from pydantic import BaseModel, UUID4
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserRetrieve(BaseModel):
    username: str
    id: UUID4
    time_created: datetime
    time_updated: datetime | None
