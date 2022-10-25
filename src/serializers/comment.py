from pydantic import UUID4, BaseModel


class CommentCreate(BaseModel):
    post_id: UUID4
    text: str


class CommentList(BaseModel):
    author_id: UUID4
    text: str
    children: list["CommentList"]

    class Config:
        orm_mode = True
