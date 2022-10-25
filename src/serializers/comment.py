from pydantic import UUID4, BaseModel


class CommentCreate(BaseModel):
    post_id: UUID4
    text: str


class CommentUpdate(BaseModel):
    text: str


class CommentList(BaseModel):
    id: UUID4
    author_id: UUID4
    text: str
    children: list["CommentList"]

    class Config:
        orm_mode = True
