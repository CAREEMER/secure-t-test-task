from datetime import datetime

from pydantic import UUID4, BaseModel


class CommentCreate(BaseModel):
    post_id: UUID4
    text: str


class CommentUpdate(BaseModel):
    text: str


class CommentRetrieve(BaseModel):
    id: UUID4
    post_id: UUID4
    text: str
    time_created: datetime
    time_updated: datetime | None


class CommentTree(CommentRetrieve):
    children: list["CommentTree"]

    class Config:
        orm_mode = True
