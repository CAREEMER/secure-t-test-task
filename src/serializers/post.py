from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str


class PostRetrieve(PostCreate):
    author_uuid: str
    created_at: datetime
    upvote_count: int
