from typing import List
from uuid import UUID

import sqlalchemy
from sqlmodel import Field, Relationship

from models.base import ModelBase
from models.user import User


class EntityBase(ModelBase):
    author_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    text: str


class Post(EntityBase, table=True):
    author: "User" = Relationship(back_populates="posts")
    upvotes: list["PostUpvote"] = Relationship(back_populates="parent_post")


class Comment(EntityBase, table=True):
    author: "User" = Relationship(back_populates="comments")
    parent_post_uuid: UUID = Field(nullable=False, foreign_key="post.uuid", index=True)
    parent_post: "Post" = Relationship(back_populates="upvotes")
    parent_comment_uuid: UUID = Field(nullable=True, foreign_key="comment.uuid")
    parent_comment: "Comment" = Relationship(back_populates="child_comment")
    child_comments: list["Comment"] = Relationship(back_populates="parent_comment")


class PostUpvote(ModelBase, table=True):
    user_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    user: "User" = Relationship(back_populates="post_upvotes")
    post_uuid: UUID = Field(nullable=False, foreign_key="post.uuid", index=True)
    post: "Post" = Relationship(back_populates="upvotes")
    positive: bool = Field(nullable=False, default=True)


class CommentUpvote(ModelBase, table=True):
    user_uuid: UUID = Field(nullable=False, foreign_key="user.uuid", index=True)
    user: "User" = Relationship(back_populates="comment_upvotes")
    comment_uuid: UUID = Field(nullable=False, foreign_key="comment.uuid", index=True)
    comment: "Comment" = Relationship(back_populates="upvotes")
    positive: bool = Field(nullable=False, default=True)
