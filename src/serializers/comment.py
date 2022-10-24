from pydantic import UUID4, BaseModel


class CommentCreate(BaseModel):
    text: str


class CommentList(CommentCreate):
    author_id: UUID4
    threads_attached_to_comment: list[UUID4]
