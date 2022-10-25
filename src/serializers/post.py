from datetime import datetime

from pydantic import UUID4, BaseModel


class PostCreate(BaseModel):
    text: str


class PostRetrieve(PostCreate):
    id: UUID4
    author_id: UUID4
    time_created: datetime
    time_updated: datetime | None
