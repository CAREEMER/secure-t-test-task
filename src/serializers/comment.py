from pydantic import BaseModel, UUID4


class CommentCreate(BaseModel):
    text: str
    parent_comment_id: UUID4 | None
    parent_post_id: UUID4 | None
