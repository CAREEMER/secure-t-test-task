from sqlalchemy import Boolean, Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class EntityBase(Base):
    __abstract__ = True

    text = Column(Text, nullable=False)


class Post(EntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)


class Comment(EntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    parent_post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False, index=True)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comment.id"), nullable=False)


class PostUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)


class CommentUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    comment_uuid = Column(UUID(as_uuid=True), ForeignKey("comment.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)
