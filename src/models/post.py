from uuid import UUID

from sqlmodel import Field

from models.base import ModelBase
from models.user import User


class EntityBase(ModelBase):
    author_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    text: str


class Post(EntityBase, table=True):
    pass


class Comment(EntityBase, table=True):
    parent_post_uuid: UUID = Field(nullable=False, foreign_key="post.uuid", index=True)
    parent_comment_uuid: UUID = Field(nullable=True, foreign_key="comment.uuid")


class PostUpvote(ModelBase):
    user_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    post_uuid: UUID = Field(nullable=False, foreign_key="post.uuid", index=True)
    positive: bool = Field(nullable=False, default=True)


class CommentUpvote(ModelBase):
    user_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    comment_uuid: UUID = Field(nullable=False, foreign_key="comment.uuid", index=True)
    positive: bool = Field(nullable=False, default=True)
