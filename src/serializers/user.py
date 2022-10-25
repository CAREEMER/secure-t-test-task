from datetime import datetime

from pydantic import UUID4, BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserRetrieve(BaseModel):
    username: str
    id: UUID4
    time_created: datetime
    time_updated: datetime | None
